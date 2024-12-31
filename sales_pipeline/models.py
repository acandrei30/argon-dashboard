from django.db import models

class SalesPipelineStage(models.TextChoices):
    PROSPECTING = 'Prospecting', 'Prospecting'
    CONSULTATION_SCHEDULED = 'Consultation Scheduled', 'Consultation Scheduled'
    UNDER_CONSIDERATION = 'Under Consideration', 'Under Consideration'
    CAREGIVER_INTERVIEW_SCHEDULED = 'Caregiver Interview Scheduled', 'Caregiver Interview Scheduled'
    CAREGIVER_CONSIDERATION = 'Caregiver Consideration', 'Caregiver Consideration'
    READY_FOR_SERVICE = 'Ready for Service', 'Ready for Service'

from django.db import models

class Lead(models.Model):
    # Existing fields
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    reason = models.TextField(null=True, blank=True)
    follow_up = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=255, default="Unknown")
    follow_up_date = models.DateField(null=True, blank=True)  # Add this field if missing
    status = models.CharField(max_length=50, null=True, blank=True)  # Add this field if missing
    stage = models.CharField(
        max_length=50,
        choices=SalesPipelineStage.choices,
        default=SalesPipelineStage.PROSPECTING,
    )
    consultation_datetime = models.DateTimeField(null=True, blank=True)

    # New fields
    relation = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=[
            ("mother", "Mother"),
            ("father", "Father"),
            ("grandmother", "Grandmother"),
            ("grandfather", "Grandfather"),
            ("friend", "Friend"),
            ("aunt", "Aunt"),
            ("uncle", "Uncle"),
            ("sibling", "Sibling"),
            ("other", "Other"),
        ],
    )
    age = models.IntegerField(null=True, blank=True)  # Ensure this is present
    medical_summary = models.TextField(null=True, blank=True)
    services_required = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class LeadNotes(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="notes")
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='lead_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notes for {self.lead.name} (Created on {self.created_at})"

class Consultation(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, related_name="consultation")
    alertness = models.CharField(max_length=50)
    lives_alone = models.CharField(max_length=10)
    house_suitable = models.CharField(max_length=10)
    speech_impairment = models.CharField(max_length=20)
    sight_impairment = models.CharField(max_length=20)
    hearing_impairment = models.CharField(max_length=20)
    locomotive_impairment = models.CharField(max_length=20)
    lifting_required = models.CharField(max_length=10)
    personal_help = models.CharField(max_length=10)
    allergies = models.TextField(blank=True, null=True)
    recent_hospitalization = models.CharField(max_length=10)
    hospitalization_reason = models.TextField(blank=True, null=True)