from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import make_aware
from datetime import datetime
from django.http import JsonResponse
from recruitment.models import Caregiver
from sales_pipeline.models import Lead, LeadNotes

def schedule_caregiver_interview(request, lead_id):
    """
    Schedule an interview for a caregiver, update the lead's stage to 'Caregiver Interview Scheduled',
    and allow scheduling multiple interviews.
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
            lead.caregiver_interview_date = interview_datetime  # Update the most recent interview date
            lead.caregiver_interview_with = caregiver

            # Update the lead's stage only if it's not already "Caregiver Interview Scheduled"
            if lead.stage != "Caregiver Interview Scheduled":
                lead.stage = "Caregiver Interview Scheduled"

            lead.save()

            # Log the interview scheduling in the lead's action trail
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
