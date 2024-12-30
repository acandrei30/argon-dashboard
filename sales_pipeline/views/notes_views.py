from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from sales_pipeline.models import Lead, LeadNotes

def add_notes(request, lead_id):
    """
    Adds a note or file to a lead.
    """
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == "POST":
        # Fetch notes and file from the request
        notes = request.POST.get("notes", "").strip()
        file = request.FILES.get("file")  # Match the `name` attribute in your HTML

        # Save the note or file to the database
        if notes or file:
            LeadNotes.objects.create(lead=lead, notes=notes, file=file)

            # Redirect to the lead profile page after successful save
            return redirect("lead_profile", lead_id=lead.id)

        # Return an error if neither notes nor file is provided
        return JsonResponse({"error": "A note or file must be provided."}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)
