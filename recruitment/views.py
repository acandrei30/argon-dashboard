from django.shortcuts import render, redirect, get_object_or_404
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

def add_caregiver(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        experience = request.POST.get("experience")
        salary_expectation = request.POST.get("salary_expectation")

        # Create a new caregiver
        Caregiver.objects.create(
            name=name,
            age=age,
            experience=experience,
            salary_expectation=salary_expectation,
            stage=PipelineStage.LEAD
        )

        # Redirect to the caregiver pipeline view
        return redirect("caregiver-pipeline")

    return render(request, "recruitment/add_caregiver.html")

# Update Caregiver Stage View
def update_stage(request, caregiver_id, new_stage):
    caregiver = get_object_or_404(Caregiver, id=caregiver_id)
    if new_stage in PipelineStage.values:
        caregiver.stage = new_stage
        caregiver.save()
    return redirect("caregiver-pipeline")

def caregiver_profile(request, caregiver_id):
    # Fetch the caregiver based on their ID
    caregiver = get_object_or_404(Caregiver, id=caregiver_id)

    if request.method == "POST":
        # Update caregiver details if the form is submitted
        caregiver.name = request.POST.get("name", caregiver.name)
        caregiver.age = request.POST.get("age", caregiver.age)
        caregiver.experience = request.POST.get("experience", caregiver.experience)
        caregiver.salary_expectation = request.POST.get("salary_expectation", caregiver.salary_expectation)
        caregiver.save()
        return redirect("caregiver-pipeline")

    return render(request, "recruitment/caregiver_profile.html", {"caregiver": caregiver})
