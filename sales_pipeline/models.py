from django.db import models

# Define the sales pipeline stages
class SalesPipelineStage(models.TextChoices):
    PROSPECTING = 'Prospecting', 'Prospecting'
    CONSULTATION_SCHEDULED = 'Consultation Scheduled', 'Consultation Scheduled'
    UNDER_CONSIDERATION = 'Under Consideration', 'Under Consideration'
    CAREGIVER_INTERVIEW_SCHEDULED = 'Caregiver Interview Scheduled', 'Caregiver Interview Scheduled'
    CAREGIVER_CONSIDERATION = 'Caregiver Consideration', 'Caregiver Consideration'
    READY_FOR_SERVICE = 'Ready for Service', 'Ready for Service'

# Define the Lead model
class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    stage = models.CharField(
        max_length=50,
        choices=SalesPipelineStage.choices,
        default=SalesPipelineStage.PROSPECTING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.stage})"
