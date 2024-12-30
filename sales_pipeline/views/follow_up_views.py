from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta
from sales_pipeline.models import Lead

def update_lead_follow_up(request, lead_id):
    """
    Handles follow-up updates for a lead.
    """
    if request.method == "POST":
        try:
            lead = get_object_or_404(Lead, id=lead_id)
            action = request.POST.get("action")
            note = request.POST.get("note")
            follow_up_days = int(request.POST.get("follow_up_days", 0))

            if action == "next_stage":
                lead.stage = "Next Stage"
                lead.follow_up_completed = True
                lead.save()
                return JsonResponse({"message": "Lead moved to the next stage!"}, status=200)

            elif action == "add_note":
                if note and follow_up_days > 0:
                    lead.notes.create(content=note)
                    lead.follow_up_date = now() + timedelta(days=follow_up_days)
                    lead.follow_up_completed = False
                    lead.save()
                    return JsonResponse({"message": "Follow-up updated with a new note!"}, status=200)

            return JsonResponse({"error": "Invalid action or parameters!"}, status=400)

        except Exception as e:
            print("Error in update_lead_follow_up:", str(e))
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method!"}, status=405)
