from .views.pipeline_views import sales_pipeline
from .views.lead_views import add_lead, lead_profile, update_stage
from .views.follow_up_views import update_lead_follow_up
from .views.notes_views import add_notes
from .views.consultation_views import update_lead_consultation
from sales_pipeline.models import Lead, SalesPipelineStage, LeadNotes, Consultation

__all__ = [
    "sales_pipeline",
    "add_lead",
    "lead_profile",
    "update_stage",
    "update_lead_follow_up",
    "add_notes",
    "update_lead_consultation",
]
