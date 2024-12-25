from django.contrib import admin
from .models import Caregiver

@admin.register(Caregiver)
class CaregiverAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "stage", "salary_expectation")
    list_filter = ("stage",)
    search_fields = ("name", "experience")
