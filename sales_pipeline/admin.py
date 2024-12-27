from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'stage', 'created_at', 'updated_at')
    list_filter = ('stage', 'created_at')
    search_fields = ('name', 'email')