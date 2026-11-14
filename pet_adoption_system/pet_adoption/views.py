from datetime import date, datetime

from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.utils import timezone

from .models import *
from .adoptions_intake_report import *

def _last_months(today, n=6):
    """First day of each of the last n months, oldest first (current month last)."""
    months, year, month = [], today.year, today.month
    for _ in range(n):
        months.append(date(year, month, 1))
        year, month = (year - 1, 12) if month == 1 else (year, month - 1)
    return months[::-1]


def _monthly_counts(queryset, field, start):
    """{first day of month: row count} for rows whose `field` date is on/after `start`."""
    rows = (queryset.filter(**{f"{field}__gte": start})
            .annotate(m=TruncMonth(field)).values("m").annotate(n=Count("id")).order_by())
    return {(r["m"].date() if isinstance(r["m"], datetime) else r["m"]): r["n"] for r in rows}

# -------------------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------------------
def dashboard(request):
    today = timezone.localdate()

    # Occupancy = pets currently in the shelter (adopted/deceased pets don't take a spot).
    shelters = list(
        Shelter.objects.annotate(
            occupancy=Count("pets", filter=Q(pets__status=PetStatus.IN_SHELTER))
        )
    )
    for shelter in shelters:
        shelter.percent = min(round(shelter.occupancy / shelter.capacity * 100), 100) if shelter.capacity else 0
        shelter.bar_class = "text-bg-danger" if shelter.percent >= 90 else "text-bg-warning" if shelter.percent >= 70 else ""
    shelters.sort(key=lambda s: (-s.percent, s.shelter_name))  # fullest first

    in_shelter = sum(s.occupancy for s in shelters)
    capacity = sum(s.capacity for s in shelters)

    month, year = {"intake_date__year": today.year, "intake_date__month": today.month}, {"intake_date__year": today.year}
    intake = Pet.objects.aggregate(month=Count("id", filter=Q(**month)), year=Count("id", filter=Q(**year)))
    done = Q(status=AdoptionStatus.COMPLETED)
    adoptions = Adoption.objects.aggregate(
        pending=Count("id", filter=Q(status=AdoptionStatus.PENDING)),
        month=Count("id", filter=done & Q(adoption_date__year=today.year, adoption_date__month=today.month)),
        year=Count("id", filter=done & Q(adoption_date__year=today.year)),
    )
    with_open_request = Pet.objects.filter(
        status=PetStatus.IN_SHELTER,
        adoptions__status__in=[AdoptionStatus.PENDING, AdoptionStatus.APPROVED],
    ).distinct().count()
    active_staff = Staff.objects.filter(status=StaffStatus.ACTIVE).count()

    # Bar chart: pets taken in vs. adoptions completed, last 6 months.
    months = _last_months(today)
    intake_by_month = _monthly_counts(Pet.objects.all(), "intake_date", months[0])
    adopted_by_month = _monthly_counts(Adoption.objects.filter(status=AdoptionStatus.COMPLETED), "adoption_date", months[0])
    chart_data = {
        "labels": [m.strftime("%b %Y") for m in months],
        "intake": [intake_by_month.get(m, 0) for m in months],
        "adopted": [adopted_by_month.get(m, 0) for m in months],
    }

    # One dict per KPI card; dashboard.html loops over this list and renders _kpi_card.html for each.
    kpis = [
        {"label": "Available for adoption", "value": in_shelter, "icon": "paw.svg",
         "sub": f"{with_open_request} with an open request"},
        {"label": "Taken in this month", "value": intake["month"], "icon": "box-open.svg",
         "sub": f"{intake['year']} so far in {today.year}"},
        {"label": "Adopted this month", "value": adoptions["month"], "icon": "gift.svg",
         "sub": f"{adoptions['year']} so far in {today.year}"},
        {"label": "Pending requests", "value": adoptions["pending"], "icon": "calendar.svg",
         "sub": "Waiting for a decision"},
        {"label": "Shelter occupancy", "value": f"{in_shelter} / {capacity}", "icon": "shelter.svg",
         "sub": f"{round(in_shelter / capacity * 100) if capacity else 0}% full"},
        {"label": "Active staff", "value": active_staff, "icon": "staffs.svg", "sub": "Currently working"},
    ]
    return render(request, "dashboard.html", {"shelters": shelters, "kpis": kpis, "chart_data": chart_data})

def new_adoption(request):
    return render(request, "new_adoption.html")

def adoption_list(request):
    return render(request, "adoptions.html")

# -------------------------------------------------------------------
# Report 1: Adoptions vs Intake Report
# -------------------------------------------------------------------
def adoption_intake_report(request):
    years = available_years()
    available_months = [(0, "All months")] + list(enumerate(calendar.month_name))[1:13]

    # Get the user's selected year and month
    selected_year = int(request.GET.get("year", years[-1]))
    selected_month = int(request.GET.get("month", 0))

    # Build the report:
    report = built_adoptions_intake(selected_year, selected_month)

    context = {
        "years": years,
        "months": available_months,
        **report
    }
    return render(request, "adoption_intake_report.html", context)

def staff_report(request):
    return render(request, "staff_report.html", {"selected_year": timezone.localdate().year})
