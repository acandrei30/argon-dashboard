from .sales_pipeline_views import sales_pipeline
from .lead_views import add_lead, lead_profile
from .stage_views import update_stage, move_backward_stage, archive_lead
from .follow_up_views import update_lead_follow_up
from .notes_views import add_notes
from .consultation_views import update_lead_consultation, start_consultation_form, save_consultation_form
from .caregiver_interview import schedule_caregiver_interview
from .clients_views import clients, mark_ready_to_service  # Import the new views
from .clients_views import save_service_details  # New import

__all__ = [
    "sales_pipeline",
    "add_lead",
    "lead_profile",
    "update_stage",
    "move_backward_stage",
    "archive_lead",
    "update_lead_follow_up",
    "add_notes",
    "update_lead_consultation",
    "start_consultation_form",
    "save_consultation_form",
    "schedule_caregiver_interview",
    "clients",  
    "mark_ready_to_service",  
    "save_service_details", 
]
