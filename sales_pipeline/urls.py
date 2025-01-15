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
    start_consultation_form, 
    save_consultation_form,
    schedule_caregiver_interview,
    consultation_options
    
)
from .views.clients_views import clients, mark_ready_to_service, save_service_details  # Updated import

urlpatterns = [
    # Pipeline-related paths
    path("pipeline/", sales_pipeline, name="sales-pipeline"),
    path("add_lead/", add_lead, name="add_lead"),
    path('start-consultation-form/<int:lead_id>/', start_consultation_form, name='start-consultation-form'),
    path('save-consultation-form/<int:lead_id>/', save_consultation_form, name='save-consultation-form'),

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
    path("consultation-options/<int:lead_id>/", consultation_options, name="consultation-options"),

    # Caregiver interview path
    path("schedule-caregiver-interview/<int:lead_id>/", schedule_caregiver_interview, name="schedule_caregiver_interview"),

    # Client-related paths
    path("clients/", clients, name="clients"),
    path("mark-ready-to-service/<int:lead_id>/", mark_ready_to_service, name="mark_ready_to_service"),
    path("save-service-details/<int:lead_id>/", save_service_details, name="save_service_details"),  # Added path

]
