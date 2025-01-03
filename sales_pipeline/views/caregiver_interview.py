from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import make_aware
from datetime import datetime
from recruitment.models import Caregiver
from sales_pipeline.models import Lead, LeadNotes, SalesPipelineStage

def schedule_caregiver_interview(request, lead_id):
    """
    Schedule an interview for a caregiver and redirect back to the lead profile page.
    """
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == "POST":
        caregiver_id = request.POST.get("caregiver_id")
        interview_date = request.POST.get("interview_date")
        interview_time = request.POST.get("interview_time")

        try:
            # Fetch caregiver
            caregiver = get_object_or_404(Caregiver, id=caregiver_id)

            # Combine date and time and make it timezone-aware
            interview_datetime = make_aware(datetime.strptime(f"{interview_date} {interview_time}", "%Y-%m-%d %H:%M"))

            # Update the lead's interview details
            lead.caregiver_interview_date = interview_datetime
            lead.caregiver_interview_with = caregiver
            lead.stage = SalesPipelineStage.CAREGIVER_INTERVIEW_SCHEDULED
            lead.save()

            # Add a note to the lead's action trail
            LeadNotes.objects.create(
                lead=lead,
                notes=f"Caregiver interview scheduled with {caregiver.name} on {interview_datetime.strftime('%Y-%m-%d %H:%M')}."
            )

            # Redirect back to the lead profile page
            return redirect("lead_profile", lead_id=lead.id)

        except Exception as e:
            # Handle any errors and return an appropriate response
            print(f"Error scheduling interview: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    # Fetch caregivers for the modal (if GET request)
    caregivers = Caregiver.objects.all()

    return render(request, "sales/caregiver_interview_modal.html", {
        "lead": lead,
        "caregivers": caregivers,
    })
