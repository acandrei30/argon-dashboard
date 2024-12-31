from django.shortcuts import render
from sales_pipeline.models import Lead, SalesPipelineStage

def sales_pipeline(request):
    """
    View to display all leads grouped by their sales pipeline stages.
    """
    try:
        # Define the stages in the pipeline
        stages = {
            SalesPipelineStage.PROSPECTING: "Prospecting",
            SalesPipelineStage.CONSULTATION_SCHEDULED: "Consultation Scheduled",
            SalesPipelineStage.UNDER_CONSIDERATION: "Under Consideration",
            SalesPipelineStage.CAREGIVER_INTERVIEW_SCHEDULED: "Caregiver Interview Scheduled",
            SalesPipelineStage.CAREGIVER_CONSIDERATION: "Caregiver Consideration",
            SalesPipelineStage.READY_FOR_SERVICE: "Ready for Service",
        }

        # Fetch leads grouped by stage, including follow_up_date
        leads_by_stage = {
            stage: list(Lead.objects.filter(stage=stage).values(
                "id", 
                "name", 
                "consultation_datetime", 
                "follow_up_date"  # Include follow-up date
            ))
            for stage in stages.keys()
        }

        return render(request, "sales/pipeline.html", {
            "leads_by_stage": leads_by_stage,
            "stages": stages,
            "SalesPipelineStage": SalesPipelineStage,
        })

    except Exception as e:
        print("Error in sales_pipeline view:", str(e))
        return render(request, "sales/error.html", {"error": str(e)})
