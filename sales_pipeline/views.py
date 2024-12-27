from django.shortcuts import render, redirect, get_object_or_404
from .models import Lead, SalesPipelineStage

# Sales Pipeline View
def sales_pipeline(request):
    stages = {
        SalesPipelineStage.PROSPECTING: "Prospecting",
        SalesPipelineStage.CONSULTATION_SCHEDULED: "Consultation Scheduled",
        SalesPipelineStage.UNDER_CONSIDERATION: "Under Consideration",
        SalesPipelineStage.CAREGIVER_INTERVIEW_SCHEDULED: "Caregiver Interview Scheduled",
        SalesPipelineStage.CAREGIVER_CONSIDERATION: "Caregiver Consideration",
        SalesPipelineStage.READY_FOR_SERVICE: "Ready for Service",
    }

    leads_by_stage = {
        stage: Lead.objects.filter(stage=stage) for stage in stages.keys()
    }

    return render(request, "sales/pipeline.html", {
        "leads_by_stage": leads_by_stage,
        "stages": stages,
    })


# Add Lead View
def add_lead(request):
    if request.method == "POST":
        # Extract form data
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        # Create a new lead
        Lead.objects.create(
            name=name,
            email=email,
            phone=phone,
            stage=SalesPipelineStage.PROSPECTING,  # Default stage
        )

        # Redirect to the sales pipeline view
        return redirect("sales-pipeline")

    return render(request, "sales/add_lead.html")

def lead_profile(request, lead_id):
    # Fetch the lead object or return a 404 error if not found
    lead = get_object_or_404(Lead, id=lead_id)

    return render(request, "sales/lead_profile.html", {"lead": lead})