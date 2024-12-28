from django.contrib import admin
from .models import Lead  # Ensure you import the Lead model

class LeadAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('name', 'phone', 'email', 'location', 'stage', 'created_at', 'updated_at')  
    # Fields to filter by in the list view
    list_filter = ('stage', 'created_at')  
    # Fields to search by in the search bar
    search_fields = ('name', 'email', 'phone', 'location')  

# Register Lead model with custom admin settings
admin.site.register(Lead, LeadAdmin)
