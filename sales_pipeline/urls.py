from django.urls import path
from .views import (
    sales_pipeline,
    add_lead,
    lead_profile,
    update_stage,
    update_lead_follow_up,
    add_notes,
    update_lead_consultation,
    archive_lead,
)

urlpatterns = [
    # Pipeline-related paths
    path("pipeline/", sales_pipeline, name="sales-pipeline"),
    path("add_lead/", add_lead, name="add_lead"),

    # Lead-specific paths
    path("lead_profile/<int:lead_id>/", lead_profile, name="lead_profile"),

    # Stage management paths
    path("update_stage/<int:lead_id>/<str:new_stage>/", update_stage, name="update-stage"),
     path("archive_lead/<int:lead_id>/", archive_lead, name="archive-lead"),  

    # Follow-up and notes paths
    path("update_follow_up/<int:lead_id>/", update_lead_follow_up, name="update-lead-follow-up"),
    path("add_notes/<int:lead_id>/", add_notes, name="add-notes"),

    # Consultation-related paths
    path("update_consultation/<int:lead_id>/", update_lead_consultation, name="update-lead-consultation"),
]
