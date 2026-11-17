from django.contrib import admin

from .models import Shelter, Species, Breed, Pet, StaffRole, Staff, Adopter, Adoption, AdoptionStatus, PetStatus


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ("shelter_name", "address", "capacity")
    search_fields = ("shelter_name", "address")

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
 
@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ("name", "species")
    list_filter = ("species",)
    search_fields = ("name",)
 
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "breed", "sex", "status", "shelter", "intake_date")
    list_filter = ("status", "shelter", "sex", "breed__species")
    search_fields = ("name", "breed__name")
 
@admin.register(StaffRole)
class StaffRoleAdmin(admin.ModelAdmin):
    list_display = ("role_name",)
    search_fields = ("role_name",)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "role", "status", "shelter", "hire_date")
    list_filter = ("role", "status", "shelter")
    search_fields = ("first_name", "last_name", "email")

@admin.register(Adopter)
class AdopterAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "contact_number")
    search_fields = ("first_name", "last_name", "email")
 
@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ("id", "pet", "adopter", "staff", "status", "request_date", "adoption_date")
    list_filter = ("status", "request_date")
    search_fields = ("pet__name", "adopter__first_name", "adopter__last_name")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # saves the adoption

        pet = obj.pet
        # Mark as adopted if adoption is completed: 
        if obj.status == AdoptionStatus.COMPLETED:
            pet.status = PetStatus.ADOPTED
        # Bring back to in shelter status if adoption was not marked as completed:
        elif pet.status == PetStatus.ADOPTED:
            pet.status = PetStatus.IN_SHELTER
        pet.save(update_fields=["status"])

    def delete_model(self, request, obj):
        pet = obj.pet
        was_completed = obj.status == AdoptionStatus.COMPLETED
        super().delete_model(request, obj)
        # Bring back to shelter if its completed adoption is deleted,
        # == Adopted avoids deceased pets from being affected.
        if was_completed and pet.status == PetStatus.ADOPTED:
            pet.status = PetStatus.IN_SHELTER
            pet.save(update_fields=["status"])