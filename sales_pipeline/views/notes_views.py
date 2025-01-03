from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from sales_pipeline.models import Lead, LeadNotes

def add_notes(request, lead_id):
    """
    Adds a note to a lead.
    """
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == "POST":
        try:
            # Extract note content and file from the request
            note_content = request.POST.get("notes", "")
            file = request.FILES.get("file")

            # Check if either note content or file is provided
            if not note_content and not file:
                return JsonResponse({"error": "A note or a file must be provided."}, status=400)

            # Create a new note entry
            LeadNotes.objects.create(
                lead=lead,
                notes=note_content,
                file=file,
            )

            # Redirect back to the lead profile page
            return redirect("lead_profile", lead_id=lead.id)

        except Exception:
            # Return error message without printing
            return JsonResponse({"error": "An unexpected error occurred while adding the note."}, status=500)

    return JsonResponse({"error": "Invalid request method!"}, status=405)
