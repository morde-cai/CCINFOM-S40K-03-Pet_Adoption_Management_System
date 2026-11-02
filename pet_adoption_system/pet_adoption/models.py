from django.db import models

# Create your models here.

IMAGE_DIR = "pets/"

# -------------------------------------------------------------------
# Enums
# -------------------------------------------------------------------
# Note: For enums, the pairs are defined as (value, label).
#       The label is for display. The all-capitals are just constant
#       class attributes.

class PetStatus(models.TextChoices):
    IN_SHELTER = 'in-shelter', 'In shelter'
    ADOPTED = 'adopted', 'Adopted'
    DECEASED = 'deceased', 'Deceased'

class AdoptionStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    COMPLETED = 'completed', 'Completed'

class StaffStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    ON_LEAVE = 'on-leave', 'On leave'
    TERMINATED = 'terminated', 'Terminated'

class Sex(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'

# -------------------------------------------------------------------
# Shelter Table
# -------------------------------------------------------------------
class Shelter(models.Model):
    id = models.AutoField(primary_key=True)
    shelter_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
 
    def __str__(self):
        return self.shelter_name

# -------------------------------------------------------------------
# Pet Tables
# -------------------------------------------------------------------
class Species(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Breed(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25) # I kept this not unique due to mixed breeds.
    species = models.ForeignKey(
        Species, on_delete=models.PROTECT, related_name="breeds"
    )

    def __str__(self):
        return self.name

class Pet(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, related_name="pets")
    status = models.CharField(
        max_length=15, choices=PetStatus.choices, default=PetStatus.IN_SHELTER
    )
    shelter = models.ForeignKey(Shelter, on_delete=models.PROTECT, related_name="pets")
    sex = models.CharField(max_length=10, choices=Sex.choices)
    date_of_birth = models.DateField(null=True, blank=True) 
    kg_weight = models.FloatField()
    intake_date = models.DateField()
    description = models.TextField(
        blank=True, help_text="Personality, health notes, and anything adopters should know."
    )
    # Needs Pillow + MEDIA_ROOT / MEDIA_URL in settings.py
    image = models.ImageField(upload_to=IMAGE_DIR, null=True, blank=True)
 
    def __str__(self):
        return self.name

# -------------------------------------------------------------------
# Staff Tables
# -------------------------------------------------------------------
class StaffRole(models.Model):
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=20, unique=True)
 
    def __str__(self):
        return self.role_name
 
class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=10, choices=Sex.choices)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    role = models.ForeignKey(
        StaffRole, on_delete=models.PROTECT, related_name="staff_members"
    )
    status = models.CharField(
        max_length=20, choices=StaffStatus.choices, default=StaffStatus.ACTIVE
    )
    shelter = models.ForeignKey(
        Shelter, on_delete=models.PROTECT, related_name="staff_members"
    )
    hire_date = models.DateField()
 
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# -------------------------------------------------------------------
# Adoption Tables
# -------------------------------------------------------------------
class Adopter(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=10, choices=Sex.choices)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
 
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Adoption(models.Model):
    id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT, related_name="adoptions")
    adopter = models.ForeignKey(
        Adopter, on_delete=models.PROTECT, related_name="adoptions"
    )
    staff = models.ForeignKey(
        Staff, on_delete=models.PROTECT, related_name="adoptions"
    )
    # TODO?: MAKE A REPORT FOR THE FEE OF EVERY SHELTER
    fee = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    request_date = models.DateField()
    adoption_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=15, choices=AdoptionStatus.choices, default=AdoptionStatus.PENDING
    )
 
    def __str__(self):
        return f"Adoption #{self.id}: {self.pet} -> {self.adopter}"
