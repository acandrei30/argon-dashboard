from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from sales_pipeline.models import Lead, SalesPipelineStage
from sales_pipeline.models import Lead, Consultation, LeadNotes 
from django.utils.timezone import now

def update_lead_consultation(request, lead_id):
    """
    Updates the consultation datetime for a lead and moves it to the 'Consultation Scheduled' stage.
    """
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == "POST":
        try:
            # Fetch consultation datetime from the request
            consultation_datetime = request.POST.get('consultation_datetime')

            # Debug: Print the received datetime
            print("Received consultation_datetime:", consultation_datetime)

            if not consultation_datetime:
                return JsonResponse({"error": "Consultation datetime is required."}, status=400)

            # Update the lead's consultation datetime and stage
            lead.consultation_datetime = consultation_datetime
            lead.stage = SalesPipelineStage.CONSULTATION_SCHEDULED
            lead.save()

            return JsonResponse({"message": "Consultation scheduled successfully!"}, status=200)

        except Exception as e:
            print("Error updating consultation datetime:", str(e))
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)

from django.shortcuts import render, get_object_or_404, redirect
from sales_pipeline.models import Lead, Consultation

def start_consultation_form(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    return render(request, "sales/consultation_form.html", {"lead": lead})

def save_consultation_form(request, lead_id):
    if request.method == "POST":
        # Fetch the lead
        lead = get_object_or_404(Lead, id=lead_id)

        # Create or update consultation for the lead
        consultation, created = Consultation.objects.get_or_create(lead=lead)
        consultation.alertness = request.POST.get("alertness")
        consultation.lives_alone = request.POST.get("lives_alone")
        consultation.house_suitable = request.POST.get("house_suitable")
        consultation.speech_impairment = request.POST.get("speech_impairment")
        consultation.sight_impairment = request.POST.get("sight_impairment")
        consultation.hearing_impairment = request.POST.get("hearing_impairment")
        consultation.locomotive_impairment = request.POST.get("locomotive_impairment")
        consultation.lifting_required = request.POST.get("lifting_required")
        consultation.personal_help = request.POST.get("personal_help")
        consultation.allergies = request.POST.get("allergies")
        consultation.recent_hospitalization = request.POST.get("recent_hospitalization")
        consultation.hospitalization_reason = request.POST.get("hospitalization_reason")
        consultation.save()

        # Update lead stage to "Under Consideration"
        lead.stage = SalesPipelineStage.UNDER_CONSIDERATION
        lead.save()

        # Add a note to the action trail
        LeadNotes.objects.create(
            lead=lead,
            notes="Consultation completed and moved to Under Consideration",
            created_at=now()
        )

        # Redirect back to lead profile
        return redirect("lead_profile", lead_id=lead.id)

    # Redirect to lead profile if not a POST request
    return redirect("lead_profile", lead_id=lead_id)