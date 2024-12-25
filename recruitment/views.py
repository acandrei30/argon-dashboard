from django.shortcuts import render, redirect
from .models import Caregiver, PipelineStage

# Caregiver Pipeline View
def caregiver_pipeline(request):
    # Define the stages of the pipeline
    stages = {
        PipelineStage.LEAD: "Lead",
        PipelineStage.TRAINING_COMPLETED: "Training Completed",
        PipelineStage.BACKGROUND_CHECK: "Background Check",
        PipelineStage.UNASSIGNED: "Unassigned Caregiver",
        PipelineStage.ACTIVE: "Active Caregiver",
    }

    # Prepare caregivers grouped by stage as a dictionary
    caregivers_by_stage = {
        stage: Caregiver.objects.filter(stage=stage) for stage in stages.keys()
    }

    # Render the pipeline page
    return render(request, "recruitment/pipeline.html", {
        "caregivers_by_stage": caregivers_by_stage,
        "stages": stages,
    })
# Add Caregiver View
def add_caregiver(request):
    if request.method == "POST":
        # Collect caregiver details from the form
        name = request.POST.get("name")
        age = request.POST.get("age")
        experience = request.POST.get("experience")
        salary_expectation = request.POST.get("salary_expectation")

        # Create a new caregiver record
        Caregiver.objects.create(
            name=name,
            age=age,
            experience=experience,
            salary_expectation=salary_expectation,
            stage=PipelineStage.LEAD  # Set the initial stage to "Lead"
        )

        # Redirect to the pipeline view after adding
        return redirect("pipeline")

    # Render the "Add Caregiver" form page for GET requests
    return render(request, "recruitment/add_caregiver.html")

# Update Caregiver Stage View
def update_stage(request, caregiver_id, new_stage):
    caregiver = get_object_or_404(Caregiver, id=caregiver_id)
    if new_stage in PipelineStage.values:
        caregiver.stage = new_stage
        caregiver.save()
    return redirect("pipeline")