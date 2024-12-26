from django.db import models

class PipelineStage(models.TextChoices):
    LEAD = 'Lead', 'Lead'
    INTERVIEW_COMPLETED = 'Interview Completed', 'Interview Completed'
    TRAINING_COMPLETED = 'Training Completed', 'Training Completed'
    BACKGROUND_CHECKED = 'Background Checked', 'Background Checked'
    READY_TO_WORK = 'Ready to Work', 'Ready to Work'

class Caregiver(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    experience = models.PositiveIntegerField()
    salary_expectation = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.CharField(
        max_length=50,
        choices=PipelineStage.choices,
        default=PipelineStage.LEAD
    )

    def __str__(self):
        return self.name

class CaregiverNotes(models.Model):
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE, related_name="notes")
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='caregiver_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notes for {self.caregiver.name} (Created on {self.created_at})"

from .models import Caregiver, PipelineStage, CaregiverNotes