import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from sales_pipeline.models import Lead, LeadNotes

def update_lead_follow_up(request, lead_id):
    """
    Handles follow-up actions: adding notes and marking follow-ups as done.
    """
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data
            note = data.get("note", "").strip()

            if not note:
                return JsonResponse({"error": "Note is required!"}, status=400)

            # Save the note
            LeadNotes.objects.create(lead=lead, notes=note)

            # Mark follow-up as done
            lead.follow_up_done = True
            lead.save()

            return JsonResponse({"message": "Follow-up updated successfully!"}, status=200)

        except Exception as e:
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method!"}, status=405)
