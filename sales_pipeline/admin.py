from django.contrib import admin
from .models import Lead

class LeadAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'name', 
        'phone', 
        'email', 
        'location', 
        'get_relation',  # Use a custom method for relation
        'age',           # Direct field access
        'stage', 
        'created_at', 
        'updated_at',
    )
    # Fields to filter by in the list view
    list_filter = ('stage', 'created_at')  # Removed relation since it isn't directly filterable
    # Fields to search by in the search bar
    search_fields = ('name', 'email', 'phone', 'location')  

    # Add a method to display relation in list_display
    def get_relation(self, obj):
        return obj.get_relation_display() if obj.relation else "N/A"
    get_relation.short_description = 'Relation'  # Label for the admin column

# Register Lead model with custom admin settings
admin.site.register(Lead, LeadAdmin)
