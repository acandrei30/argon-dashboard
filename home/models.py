from django.contrib.auth.models import AbstractUser
from django.db import models

# Role Choices
ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('client', 'Client'),
    ('caregiver', 'Caregiver'),
    ('care_manager', 'Care Manager'),
)

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Avoid conflicts with default User model
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Avoid conflicts with default User model
        blank=True,
    )

    def __str__(self):
        return self.username


class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Caregiver(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    certifications = models.TextField(blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.user.username


class CareManager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    region = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
