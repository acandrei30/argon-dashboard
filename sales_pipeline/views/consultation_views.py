from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from sales_pipeline.models import Lead, SalesPipelineStage

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
