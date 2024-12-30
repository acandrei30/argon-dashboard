from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from sales_pipeline.models import Lead, LeadNotes

def add_notes(request, lead_id):
    """
    Adds notes or files to a lead.
    """
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == "POST":
        try:
            note_content = request.POST.get("note", "")
            file = request.FILES.get("file")

            if note_content or file:
                LeadNotes.objects.create(lead=lead, content=note_content, file=file)
                return JsonResponse({"message": "Note added successfully!"}, status=201)

            return JsonResponse({"error": "Note or file is required!"}, status=400)

        except Exception as e:
            print("Error adding note:", str(e))
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method!"}, status=405)
