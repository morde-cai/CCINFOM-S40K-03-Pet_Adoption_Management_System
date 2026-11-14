from django.utils import timezone
from django.db.models import Min
from django.db.models import Count

import calendar

from .models import *

# -----------------------------------------------------------------------------------
# HELPER Functions
# -----------------------------------------------------------------------------------

def available_years():
    # Get the earliest completed adoption.
    earliest_adoption = Adoption.objects.filter (
        status=AdoptionStatus.COMPLETED
     # use Django's built-in aggregation function,
     # ['adoption_date__min'] gets the value directly from the dict.
    ).aggregate(Min('adoption_date'))['adoption_date__min']
    # Prevent None comparisons:
    if not earliest_adoption:
            earliest_adoption = timezone.localdate()

    earliest_intake = Pet.objects.aggregate(Min('intake_date'))['intake_date__min']
    if not earliest_intake:
        earliest_intake = timezone.localdate()
    
    earliest_date = min(earliest_adoption, earliest_intake)
    
    # Available years = Earliest record's year -> this year
    available_years = range(
        earliest_date.year,
        timezone.localdate().year + 1
    )

    return available_years

def species_charts_data(intakes, adoptions):
    # Get the intake counts per species:
    # Dict of {species name: row count}
    intake_species = {}
    for row in intakes.values("breed__species__name").annotate(total=Count("id")):
        # Takes the values directly instead of the query set of dictionaries
        intake_species[row["breed__species__name"]] = row["total"]
    
    # Get adoption counts per species
    adoption_species = {}
    for row in adoptions.values("pet__breed__species__name").annotate(total=Count("id")):
        adoption_species[row["pet__breed__species__name"]] = row["total"]
        
    # 1. Prepare the charts label list:
    species_list = []
    for species in intake_species:
        species_list.append(species)
    for species in adoption_species:
        if species not in species_list: # skip ones already added
            species_list.append(species)

    # 2. Prepare the charts dataset of counts:
    intake_list = []
    adopted_list = []
    for species in species_list:
        intake_list.append(intake_species.get(species, 0))
        adopted_list.append(adoption_species.get(species, 0))

    return {
        "labels": species_list,
        "intake": intake_list,
        "adopted": adopted_list,
    }

def kpi(intakes, adoptions, period_label):
    intake_count = intakes.count()
    adoption_count = adoptions.count()
    if intake_count == 0:
        ratio = "0.00%"
    else:
        ratio = f"{round(adoption_count / intake_count*100, 2):.2f}%"

    kpis = [
        {"label": "Total pets adopted", "value": adoption_count, "icon": "gift.svg", "sub": period_label},
        {"label": "Total pets taken in", "value": intake_count, "icon": "box-open.svg", "sub": period_label},
        {"label": "Ratio of Adopted to Intakes", "value": ratio, "icon": "percent.svg", "sub": period_label},
    ]

    return kpis

# -----------------------------------------------------------------------------------
# Adoptions vs Intake Report Builder
# -----------------------------------------------------------------------------------
def built_adoptions_intake(selected_year, selected_month):
    # Get the intakes and adoptions at selected year:
    intakes = Pet.objects.filter(intake_date__year=selected_year)
    adoptions = Adoption.objects.filter(
        status=AdoptionStatus.COMPLETED, adoption_date__year=selected_year
    )
    period_label = str(selected_year) # Year label for KPIs

    # Get the intakes and adoptions at selected month:
    if selected_month: # If non-zero, meaning a specific month and not all months
        intakes = intakes.filter(intake_date__month=selected_month)
        adoptions = adoptions.filter(adoption_date__month=selected_month)

        # Add month to label if it's not 0 (which means All Months)
        period_label = f"{calendar.month_name[selected_month]} {selected_year}" 

    kpis = kpi(intakes, adoptions, period_label)
    
    chart_data = species_charts_data(intakes, adoptions)

    return {
        "period_label": period_label,
        "kpis": kpis,
        "chart_data": chart_data
    }