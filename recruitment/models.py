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
