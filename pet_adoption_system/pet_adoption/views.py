
from datetime import date, datetime

from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.utils import timezone
import calendar
from .models import *


def _last_months(today, n=6):
    """First day of each of the last n months, oldest first."""
    months, year, month = [], today.year, today.month

    for _ in range(n):
        months.append(date(year, month, 1))
        year, month = (year - 1, 12) if month == 1 else (year, month - 1)

    return months[::-1]


def _monthly_counts(queryset, field, start):
    """Count records grouped by month."""
    rows = (
        queryset.filter(**{f"{field}__gte": start})
        .annotate(m=TruncMonth(field))
        .values("m")
        .annotate(n=Count("id"))
        .order_by()
    )

    return {
        r["m"].date() if isinstance(r["m"], datetime) else r["m"]: r["n"]
        for r in rows
    }


def dashboard(request):
    today = timezone.localdate()

    shelters = list(
        Shelter.objects.annotate(
            occupancy=Count(
                "pets",
                filter=Q(pets__status=PetStatus.IN_SHELTER)
            )
        )
    )

    for shelter in shelters:
        shelter.percent = (
            min(round(shelter.occupancy / shelter.capacity * 100), 100)
            if shelter.capacity else 0
        )
        shelter.bar_class = (
            "text-bg-danger" if shelter.percent >= 90
            else "text-bg-warning" if shelter.percent >= 70
            else ""
        )

    shelters.sort(key=lambda s: (-s.percent, s.shelter_name))

    in_shelter = sum(s.occupancy for s in shelters)
    capacity = sum(s.capacity for s in shelters)

    month = {
        "intake_date__year": today.year,
        "intake_date__month": today.month
    }
    year = {"intake_date__year": today.year}

    intake = Pet.objects.aggregate(
        month=Count("id", filter=Q(**month)),
        year=Count("id", filter=Q(**year))
    )

    done = Q(status=AdoptionStatus.COMPLETED)

    adoptions = Adoption.objects.aggregate(
        pending=Count("id", filter=Q(status=AdoptionStatus.PENDING)),
        month=Count(
            "id",
            filter=done & Q(
                adoption_date__year=today.year,
                adoption_date__month=today.month
            )
        ),
        year=Count(
            "id",
            filter=done & Q(adoption_date__year=today.year)
        )
    )

    with_open_request = Pet.objects.filter(
        status=PetStatus.IN_SHELTER,
        adoptions__status__in=[
            AdoptionStatus.PENDING,
            AdoptionStatus.APPROVED
        ]
    ).distinct().count()

    active_staff = Staff.objects.filter(
        status=StaffStatus.ACTIVE
    ).count()

    months = _last_months(today)

    intake_by_month = _monthly_counts(
        Pet.objects.all(), "intake_date", months[0]
    )

    adopted_by_month = _monthly_counts(
        Adoption.objects.filter(status=AdoptionStatus.COMPLETED),
        "adoption_date",
        months[0]
    )

    chart_data = {
        "labels": [m.strftime("%b %Y") for m in months],
        "intake": [intake_by_month.get(m, 0) for m in months],
        "adopted": [adopted_by_month.get(m, 0) for m in months],
    }

    kpis = [
        {
            "label": "Available for adoption",
            "value": in_shelter,
            "icon": "paw.svg",
            "sub": f"{with_open_request} with an open request"
        },
        {
            "label": "Taken in this month",
            "value": intake["month"],
            "icon": "box-open.svg",
            "sub": f"{intake['year']} so far in {today.year}"
        },
        {
            "label": "Adopted this month",
            "value": adoptions["month"],
            "icon": "gift.svg",
            "sub": f"{adoptions['year']} so far in {today.year}"
        },
        {
            "label": "Pending requests",
            "value": adoptions["pending"],
            "icon": "calendar.svg",
            "sub": "Waiting for a decision"
        },
        {
            "label": "Shelter occupancy",
            "value": f"{in_shelter} / {capacity}",
            "icon": "shelter.svg",
            "sub": f"{round(in_shelter / capacity * 100) if capacity else 0}% full"
        },
        {
            "label": "Active staff",
            "value": active_staff,
            "icon": "staffs.svg",
            "sub": "Currently working"
        },
    ]

    return render(request, "dashboard.html", {
        "shelters": shelters,
        "kpis": kpis,
        "chart_data": chart_data
    })



def new_adoption(request):
    error = ""

    if request.method == "POST":
        pet_id = request.POST.get("pet")
        adopter_id = request.POST.get("adopter")
        staff_id = request.POST.get("staff")
        request_date = request.POST.get("request_date")
        adoption_date = request.POST.get("adoption_date") or None
        status = request.POST.get("status")

        pet = Pet.objects.filter(
            id=pet_id,
            status=PetStatus.IN_SHELTER
        ).first()

        if not pet:
            error = "This pet is not available for adoption."

        elif Adoption.objects.filter(
            pet_id=pet_id,
            status__in=[
                AdoptionStatus.PENDING,
                AdoptionStatus.APPROVED,
            ]
        ).exists():
            error = "This pet already has an active adoption request."

        elif not Adopter.objects.filter(id=adopter_id).exists():
            error = "Please select a valid adopter."

        elif not Staff.objects.filter(
            id=staff_id,
            status=StaffStatus.ACTIVE
        ).exists():
            error = "Please select an active staff member."

        else:
            adoption = Adoption.objects.create(
                pet=pet,
                adopter_id=adopter_id,
                staff_id=staff_id,
                request_date=request_date,
                adoption_date=adoption_date,
                status=status,
            )

            if adoption.status == AdoptionStatus.COMPLETED:
                pet.status = PetStatus.ADOPTED
                pet.save(update_fields=["status"])

            return redirect("adoption_list")

    return render(request, "new_adoption.html", {
        "pets": Pet.objects.filter(status=PetStatus.IN_SHELTER),
        "adopters": Adopter.objects.all(),
        "staff_members": Staff.objects.filter(
            status=StaffStatus.ACTIVE
        ),
        "statuses": AdoptionStatus.choices,
        "error": error,
    })


def adoption_list(request):
    adoptions = Adoption.objects.select_related(
        "pet", "adopter", "staff"
    ).all()

    selected_status = request.GET.get("status", "")
    selected_staff = request.GET.get("staff", "")
    selected_date = request.GET.get("adoption_date", "")

    if selected_status in dict(AdoptionStatus.choices):
        adoptions = adoptions.filter(status=selected_status)
    elif selected_status:
        selected_status = ""

    if selected_staff:
        if selected_staff.isdigit():
            adoptions = adoptions.filter(staff_id=selected_staff)
        else:
            selected_staff = ""

    if selected_date:
        try:
            datetime.strptime(selected_date, "%Y-%m-%d")
            adoptions = adoptions.filter(adoption_date=selected_date)
        except ValueError:
            selected_date = ""

    staff_members = Staff.objects.all().order_by(
        "first_name", "last_name"
    )

    return render(request, "adoptions.html", {
        "adoptions": adoptions.order_by("-request_date"),
        "staff_members": staff_members,
        "statuses": AdoptionStatus.choices,
        "selected_status": selected_status,
        "selected_staff": selected_staff,
        "selected_date": selected_date,
    })
def edit_adoption(request, pk):
    adoption = Adoption.objects.select_related("pet").filter(pk=pk).first()

    if not adoption:
        return redirect("adoption_list")

    if request.method == "POST":
        status = request.POST.get("status")
        adoption_date = request.POST.get("adoption_date") or None

        if status not in dict(AdoptionStatus.choices):
            return render(request, "edit_adoption.html", {
                "adoption": adoption,
                "statuses": AdoptionStatus.choices,
                "error": "Invalid adoption status."
            })

        adoption.status = status
        adoption.adoption_date = adoption_date
        adoption.save()

        if status == AdoptionStatus.COMPLETED:
            adoption.pet.status = PetStatus.ADOPTED
        else:
            adoption.pet.status = PetStatus.IN_SHELTER

        adoption.pet.save(update_fields=["status"])

        return redirect("adoption_list")

    return render(request, "edit_adoption.html", {
        "adoption": adoption,
        "statuses": AdoptionStatus.choices,
    })

def adoption_intake_report(request):
    today = timezone.localdate()

    try:
        selected_year = int(request.GET.get("year", today.year))
    except (ValueError, TypeError):
        selected_year = today.year

    month_value = request.GET.get("month", "")

    pets = Pet.objects.filter(intake_date__year=selected_year)

    if month_value:
        try:
            selected_month = int(month_value)
            if 1 <= selected_month <= 12:
                pets = pets.filter(intake_date__month=selected_month)
            else:
                month_value = ""
        except (ValueError, TypeError):
            month_value = ""

    total_intake = pets.count()

    species_data = list(
        pets.values("breed__species__name")
        .annotate(total=Count("id"))
        .order_by("breed__species__name")
    )

    monthly_data = (
        Pet.objects.filter(intake_date__year=selected_year)
        .annotate(month_number=ExtractMonth("intake_date"))
        .values("month_number")
        .annotate(total=Count("id"))
        .order_by("month_number")
    )

    monthly_lookup = {
        item["month_number"]: item["total"]
        for item in monthly_data
    }

    monthly_labels = [
        calendar.month_abbr[month]
        for month in range(1, 13)
    ]

    monthly_values = [
        monthly_lookup.get(month, 0)
        for month in range(1, 13)
    ]

    intake_records = pets.select_related(
        "breed", "breed__species", "shelter"
    ).order_by("-intake_date", "name")

    available_years = sorted(
        {d.year for d in Pet.objects.dates("intake_date", "year")}
        | {today.year},
        reverse=True
    )

    months = [
        (number, calendar.month_name[number])
        for number in range(1, 13)
    ]

    selected_month_name = (
        calendar.month_name[int(month_value)]
        if month_value else "All Months"
    )

    top_species = max(
        species_data,
        key=lambda item: item["total"],
        default=None
    )

    context = {
        "selected_year": selected_year,
        "selected_month": month_value,
        "selected_month_name": selected_month_name,
        "years": available_years,
        "months": months,
        "total_intake": total_intake,
        "species_data": species_data,
        "intake_records": intake_records,

        # Chart data
        "monthly_labels": monthly_labels,
        "monthly_values": monthly_values,
        "species_labels": [
            item["breed__species__name"] for item in species_data
        ],
        "species_values": [
            item["total"] for item in species_data
        ],

        # Insights
        "top_species": top_species,
        "average_monthly_intake": round(
            sum(monthly_values) / 12, 1
        ),
    }

    return render(
        request,
        "adoption_intake_report.html",
        context
    )


def staff_report(request):
    return render(request, "staff_report.html", {
        "selected_year": timezone.localdate().year
    })
