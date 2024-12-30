from .sales_pipeline_views import sales_pipeline
from .lead_views import add_lead, lead_profile
from .stage_views import update_stage, move_backward_stage, archive_lead
from .follow_up_views import update_lead_follow_up
from .notes_views import add_notes
from .consultation_views import update_lead_consultation

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
]
