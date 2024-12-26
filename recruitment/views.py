from django.shortcuts import render, redirect, get_object_or_404
from .models import Caregiver, PipelineStage

# Caregiver Pipeline View
def caregiver_pipeline(request):
    # Define the stages of the pipeline
    stages = {
        PipelineStage.LEAD: "Lead",
        PipelineStage.INTERVIEW_COMPLETED: "Interview Completed",
        PipelineStage.TRAINING_COMPLETED: "Training Completed",
        PipelineStage.BACKGROUND_CHECKED: "Background Checked",
        PipelineStage.READY_TO_WORK: "Ready to Work",
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

    if request.method == "POST":
        caregiver.stage = new_stage
        caregiver.save()
        return redirect("caregiver_profile", caregiver_id=caregiver.id)

    return JsonResponse({"error": "Invalid request method."}, status=405)

def caregiver_profile(request, caregiver_id):
    caregiver = get_object_or_404(Caregiver, id=caregiver_id)

    # Define the pipeline stages in order
    stages = [
        PipelineStage.LEAD,
        PipelineStage.INTERVIEW_COMPLETED,
        PipelineStage.TRAINING_COMPLETED,
        PipelineStage.BACKGROUND_CHECKED,
        PipelineStage.READY_TO_WORK,
    ]

    # Determine the current and next stage
    current_stage_index = stages.index(caregiver.stage) if caregiver.stage in stages else -1
    next_stage = stages[current_stage_index + 1] if current_stage_index + 1 < len(stages) else None

    # Label for the button
    next_action_label = f"Move to {next_stage}" if next_stage else None

    if request.method == "POST":
        caregiver.name = request.POST.get("name", caregiver.name)
        caregiver.age = request.POST.get("age", caregiver.age)
        caregiver.experience = request.POST.get("experience", caregiver.experience)
        caregiver.salary_expectation = request.POST.get("salary_expectation", caregiver.salary_expectation)
        caregiver.save()
        return redirect("caregiver-pipeline")

    return render(request, "recruitment/caregiver_profile.html", {
        "caregiver": caregiver,
        "next_action_label": next_action_label,
        "next_stage": next_stage,
    })
