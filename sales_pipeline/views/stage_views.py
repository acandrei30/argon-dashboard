from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from sales_pipeline.models import Lead, SalesPipelineStage


from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from sales_pipeline.models import Lead, SalesPipelineStage

def update_stage(request, lead_id, new_stage):
    """
    Updates the sales pipeline stage for a given lead.
    """
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == "POST":
        if new_stage not in SalesPipelineStage.values:
            return JsonResponse({"error": "Invalid stage."}, status=400)

        lead.stage = new_stage
        lead.save()
        return JsonResponse({"message": f"Lead stage updated to {new_stage}."}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=405)


def move_backward_stage(request, lead_id):
    """
    Moves a lead backward in the sales pipeline stages.
    """
    lead = get_object_or_404(Lead, id=lead_id)

    # Define pipeline stages in order
    stages = [
        SalesPipelineStage.PROSPECTING,
        SalesPipelineStage.CONSULTATION_SCHEDULED,
        SalesPipelineStage.UNDER_CONSIDERATION,
        SalesPipelineStage.CAREGIVER_INTERVIEW_SCHEDULED,
        SalesPipelineStage.CAREGIVER_CONSIDERATION,
        SalesPipelineStage.READY_FOR_SERVICE,
    ]

    try:
        current_index = stages.index(lead.stage)
        if current_index > 0:
            # Move the lead backward by one stage
            lead.stage = stages[current_index - 1]
            lead.save()
            return JsonResponse({"message": "Lead moved to the previous stage."}, status=200)

        return JsonResponse({"error": "Lead is already at the earliest stage."}, status=400)

    except Exception as e:
        print("Error in move_backward_stage view:", str(e))
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)


def archive_lead(request, lead_id):
    """
    Archives a lead by deleting it.
    """
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == "POST":
        try:
            lead.delete()
            return JsonResponse({"message": "Lead archived successfully!"}, status=200)

        except Exception as e:
            print("Error in archive_lead view:", str(e))
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method!"}, status=405)

def archive_lead(request, lead_id):
    """
    Archives a lead by deleting it.
    """
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == "POST":
        try:
            lead.delete()
            return JsonResponse({"message": "Lead archived successfully!"}, status=200)

        except Exception as e:
            print("Error in archive_lead view:", str(e))
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method!"}, status=405)