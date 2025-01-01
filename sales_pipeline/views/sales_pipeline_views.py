from django.shortcuts import render
from sales_pipeline.models import Lead, SalesPipelineStage
from datetime import date

def sales_pipeline(request):
    # Define the stages in the pipeline
    stages = {
        SalesPipelineStage.PROSPECTING: "Prospecting",
        SalesPipelineStage.CONSULTATION_SCHEDULED: "Consultation Scheduled",
        SalesPipelineStage.UNDER_CONSIDERATION: "Under Consideration",
        SalesPipelineStage.CAREGIVER_INTERVIEW_SCHEDULED: "Caregiver Interview Scheduled",
        SalesPipelineStage.CAREGIVER_CONSIDERATION: "Caregiver Consideration",
        SalesPipelineStage.READY_FOR_SERVICE: "Ready for Service",
    }

    # Fetch leads grouped by stage
    leads_by_stage = {
        stage: list(Lead.objects.filter(stage=stage).values(
            "id", 
            "name", 
            "consultation_datetime", 
            "follow_up_date"
        ))
        for stage in stages.keys()
    }

    return render(request, "sales/pipeline.html", {
        "leads_by_stage": leads_by_stage,
        "stages": stages,
        "SalesPipelineStage": SalesPipelineStage,
        "today": date.today(),
    })
