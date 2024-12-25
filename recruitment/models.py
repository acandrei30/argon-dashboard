from django.db import models

class PipelineStage(models.TextChoices):
    LEAD = 'Lead'
    TRAINING_COMPLETED = 'Training Completed'
    BACKGROUND_CHECK = 'Background Check'
    UNASSIGNED = 'Unassigned Caregiver'
    ACTIVE = 'Active Caregiver'

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
