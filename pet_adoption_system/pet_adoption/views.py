from datetime import date, datetime

from django.db.models import Count, Q, Sum
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.paginator import Paginator

from .models import *
from .adoptions_intake_report import *

# Use for multiple top performers
from django.utils.html import escape
from django.utils.safestring import mark_safe

# -------------------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------------------
def _dashboard_kpis():
    present = timezone.localdate()

    # Adoption Requests KPI
    available_adoptions = Pet.objects.filter(status=PetStatus.IN_SHELTER).count()
    open_requests = Adoption.objects.filter(status=AdoptionStatus.PENDING).count()

    # Intake KPI
    intake_month = Pet.objects.filter(intake_date__year=present.year,
        intake_date__month = present.month).count()
    intake_year = Pet.objects.filter(intake_date__year = present.year).count()

    # Adopted KPI
    adopted_month = Adoption.objects.filter(status=AdoptionStatus.COMPLETED, 
        adoption_date__year=present.year, adoption_date__month=present.month).count()
    adopted_year = Adoption.objects.filter(status=AdoptionStatus.COMPLETED, 
        adoption_date__year = present.year).count()

    # Pending KPI
    pending_requests = Adoption.objects.filter(status=AdoptionStatus.PENDING).count()

    # Shelter KPI
    in_shelter = available_adoptions
    capacity = Shelter.objects.aggregate(total=Sum("capacity"))["total"]

    # Active Staff KPI
    active_staff = Staff.objects.filter(status=StaffStatus.ACTIVE).count()

    # One dict per KPI card; dashboard.html loops over this list and renders _kpi_card.html for each.
    kpis = [
        {"label": "Available for adoption", "value": available_adoptions, "icon": "paw.svg",
            "sub": f"{open_requests} with an open request"},
        {"label": "Taken in this month", "value": intake_month, "icon": "box-open.svg",
            "sub": f"{intake_year} so far in {present.year}"},
        {"label": "Adopted this month", "value": adopted_month, "icon": "gift.svg",
            "sub": f"{adopted_year} so far in {present.year}"},
        {"label": "Pending requests", "value": pending_requests, "icon": "calendar.svg",
            "sub": "Waiting for a decision"},
        {"label": "Shelter occupancy", "value": f"{in_shelter} / {capacity}", "icon": "shelter.svg",
            "sub": f"{round(in_shelter / capacity * 100) if capacity else 0}% full"},
        {"label": "Active staff", "value": active_staff, "icon": "staffs.svg", "sub": "Currently working"},
    ]

    return kpis

def _dashboard_shelter():
    # Get the count of pets per shelter:
    # New object variable: Occupancy = pets in shelter (adopted/deceased pets don't take a spot).
    shelters = list(
        Shelter.objects.annotate(
            # Use related name "pets" from models.py:
            occupancy=Count("pets", filter=Q(pets__status=PetStatus.IN_SHELTER))
        )
    )

    # Get the percantages (make new object variables: percent, bar_class):
    for shelter in shelters:
        if shelter.capacity:
            shelter.percent = round(shelter.occupancy / shelter.capacity * 100)
        else:
            shelter.percent = 0

        if shelter.percent >=90:
            shelter.bar_class = "text-bg-danger"
        elif shelter.percent >= 70:
            shelter.bar_class = "text-bg-warning"
        else:
            shelter.bar_class = ""

    # Sort by fullest first (percent in descending order), then name (in ascending order)
    shelters.sort(key=lambda s: (-s.percent, s.shelter_name))

    return shelters

def _dashboard_bar():
    present = timezone.localdate()
    labels, intake, adopted = [], [], []

    # go from 5 months ago up to this month
    for i in range(5, -1, -1):
        month = present.month - i
        year = present.year

        # If month is from last year:
        if month <= 0:
            month += 12
            year -= 1

        labels.append(date(year, month, 1).strftime("%b %Y"))
        intake.append(Pet.objects.filter(
            intake_date__year=year, intake_date__month=month).count())
        adopted.append(Adoption.objects.filter(
            status=AdoptionStatus.COMPLETED,
            adoption_date__year=year, adoption_date__month=month).count())

    chart_data = {
        "labels": labels, 
        "intake": intake,
        "adopted": adopted
    }

    return chart_data
    
def dashboard(request):
    shelters = _dashboard_shelter()    
    kpis = _dashboard_kpis()
    chart_data = _dashboard_bar()
    
    context = {
        "shelters": shelters,
        "kpis": kpis,
        "chart_data": chart_data
    }

    return render(request, "dashboard.html", context)

# -------------------------------------------------------------------
# New Adoptions
# -------------------------------------------------------------------
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

# -------------------------------------------------------------------
# Adoptions List and Edit Adoptions
# -------------------------------------------------------------------
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

# -------------------------------------------------------------------
# Report 1: Adoptions vs Intake
# -------------------------------------------------------------------
def adoption_intake_report(request):
    years = available_years()
    available_months = [(0, "All months")] + list(enumerate(calendar.month_name))[1:13]

    # Get the user's selected year and month
    selected_year = int(request.GET.get("year", years[0]))
    selected_month = int(request.GET.get("month", 0))

    # Build the report:
    report = built_adoptions_intake(selected_year, selected_month)

    context = {
        "years": years,
        "months": available_months,
        "selected_year": selected_year,
        "selected_month": selected_month,
        **report
    }
    return render(request, "adoption_intake_report.html", context)

# -------------------------------------------------------------------
# Report 2: Staff Adoptions
# -------------------------------------------------------------------

def _requested_year(request):
    year_param = request.GET.get('year')
    if not year_param or not year_param.isdigit():
        return date.today().year
    return int(year_param)

STAFF_PAGE_SIZE = 100 # limit to 100 at a time so it doesnt load all of the DB's records
STAFF_CHART_SIZE = 10 # max number of staff for the chart

def staff_report(request):
    year = _requested_year(request)

    completed = Adoption.objects.filter(status=AdoptionStatus.COMPLETED, adoption_date__isnull=False)
    available_years = [d.year for d in completed.dates("adoption_date", "year", order="DESC")]
    if year not in available_years:
        available_years = sorted(available_years + [year], reverse=True)

    # Filter adoptions by status and year
    # MYSQL: WHERE status = 'Completed' AND YEAR(adoption_date) = <year>
    handled_in_year = Q(
                        adoptions__status = AdoptionStatus.COMPLETED, adoptions__adoption_date__year = year
    )

    """
    SELECT s.id, s.first_name, s.last_name, COUNT(a.id) AS pets_handled
    FROM staff s
    LEFT JOIN adoptions a 
        ON s.id = a.staff_id
            AND a.status = 'COMPLETED'
            AND a.adoption_date BETWEEN <year_first_day> AND <year_last_day>
    GROUP BY
        s.id, s.last_name, s.first_name
    ORDER BY
        pets_handled DESC, s.last_name ASC, s.first_name ASC;
    """

    ranks = (
        Staff.objects.select_related("role", "shelter")
        .annotate(pets_handled=Count("adoptions", filter=handled_in_year))
        .order_by("-pets_handled", "last_name", "first_name", "id")
    )

    # Chart
    top_ten = list(ranks[:STAFF_CHART_SIZE])
    chart_data = {
        "labels": [str(staff) for staff in top_ten],
        "values": [staff.pets_handled for staff in top_ten],
    }

    # Table
    paginator = Paginator(ranks, STAFF_PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))
    page_range = list(paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1))

    previous_pets_handled = None
    previous_rank = None
    for position, staff in enumerate(page_obj, start=page_obj.start_index()):
        if staff.pets_handled == previous_pets_handled:
            staff.rank = previous_rank
        else:
            staff.rank = position
            previous_rank = position
        previous_pets_handled = staff.pets_handled

    # Total count per year
    total_handled = sum(staff.pets_handled for staff in ranks)
    top = top_ten[0] if top_ten and top_ten[0].pets_handled else None

    # Calculates the top Perfomer
    top_pets_handled = top_ten[0].pets_handled if top_ten else 0
    top_performers = ([staff for staff in ranks if staff.pets_handled == top_pets_handled] if top_pets_handled else [])


    kpis = [
        {"label": f"Total Adoptions Handled in {year}", 
         "value": total_handled,
         "icon": "paw.svg",
         "sub": f"Completed across {paginator.count} staff members"},

        {"label": "Top Performer" if len(top_performers) == 1 else "Top Performers", 
         "value": mark_safe(",<br>".join(escape(str(staff)) for staff in top_performers)) if top_performers else "No adoptions yet",
         "icon": "gift.svg",
         "sub": f"Handled {top_pets_handled} adoptions in {year}" if top_performers else f"No completed adoptions in {year}"},

        {"label": "Staff on Record", 
         "value": paginator.count, "icon": 
         "staffs.svg",
         "sub": "across all shelters"},
    ]

    return render(request, "staff_report.html", {
        "selected_year": year,
        "available_years": available_years,
        "page_obj": page_obj,
        "kpis": kpis,
        "chart_data": chart_data,
        "page_range": page_range,
    })
