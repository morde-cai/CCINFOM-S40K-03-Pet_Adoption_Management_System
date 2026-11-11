from datetime import date, datetime

from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator

from .models import *


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

def adoption_intake_report(request):
    today = timezone.localdate()  # defaults until the year/month selector is built
    return render(request, "adoption_intake_report.html", {
        "selected_year": today.year,
        "selected_month_name": today.strftime("%B"),
    })

# Staff Adoptions Report

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
    for rank, staff in enumerate(page_obj, start=page_obj.start_index()):
        staff.rank = rank

    # Total count per year
    total_handled = sum(staff.pets_handled for staff in ranks)
    top = top_ten[0] if top_ten and top_ten[0].pets_handled else None


    kpis = [
        {"label": f"Total Adoptions Handled in {year}", "value": total_handled, "icon": "paw.svg",
        "sub": f"Completed across {paginator.count} staff members"},

        {"label": "Top Performer", "value": str(top) if top else "No adoptions yet", "icon": "gift.svg",
        "sub": f"Handled {top.pets_handled} adoptions in {year}" if top else f"No completed adoptions in {year}"},

        {"label": "Staff on Record", "value": paginator.count, "icon": "staffs.svg",
        "sub": "across all shelters"},
    ]

    return render(request, "staff_report.html", {
        "selected_year": year,
        "available_years": available_years,
        "ranks": page_obj,  
        "page_obj": page_obj,
        "kpis": kpis,
        "chart_data": chart_data,
    })
