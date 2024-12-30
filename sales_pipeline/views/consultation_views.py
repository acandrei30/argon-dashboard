from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from sales_pipeline.models import Lead

def update_lead_consultation(request, lead_id):
    """
    Updates the consultation date and time for a lead.
    """
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == "POST":
        try:
            consultation_datetime = request.POST.get('consultation_datetime')

            # Print out what the backend is receiving
            print("Received consultation_datetime:", consultation_datetime)

            if not consultation_datetime:
                return JsonResponse({"error": "Consultation datetime is required."}, status=400)

            # Ensure the format matches what's expected
            lead.consultation_datetime = consultation_datetime
            lead.stage = SalesPipelineStage.CONSULTATION_SCHEDULED
            lead.save()

            return JsonResponse({"message": "Consultation scheduled successfully!"}, status=200)

        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method!"}, status=405)
