from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Caregiver, PipelineStage
from .models import Caregiver, PipelineStage, CaregiverNotes

# Caregiver Pipeline View
def caregiver_pipeline(request):
    stages = {
        PipelineStage.LEAD: "Lead",
        PipelineStage.INTERVIEW_COMPLETED: "Interview Completed",
        PipelineStage.TRAINING_COMPLETED: "Training Completed",
        PipelineStage.BACKGROUND_CHECKED: "Background Checked",
        PipelineStage.READY_TO_WORK: "Ready to Work",
    }

    caregivers_by_stage = {
        stage: Caregiver.objects.filter(stage=stage) for stage in stages.keys()
    }

    return render(request, "recruitment/pipeline.html", {
        "caregivers_by_stage": caregivers_by_stage,
        "stages": stages,
    })

# Add Caregiver
def add_caregiver(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        experience = request.POST.get("experience")
        salary_expectation = request.POST.get("salary_expectation")

        Caregiver.objects.create(
            name=name,
            age=age,
            experience=experience,
            salary_expectation=salary_expectation,
            stage=PipelineStage.LEAD
        )

        return redirect("caregiver-pipeline")

    return render(request, "recruitment/add_caregiver.html")

# Update Caregiver Stage View
def update_stage(request, caregiver_id, new_stage):
    caregiver = get_object_or_404(Caregiver, id=caregiver_id)
    if request.method == "POST" and new_stage in PipelineStage.values:
        caregiver.stage = new_stage
        caregiver.save()
        return redirect("caregiver_profile", caregiver_id=caregiver.id)

    return JsonResponse({"error": "Invalid request."}, status=400)

# Caregiver Profile View
def caregiver_profile(request, caregiver_id):
    caregiver = get_object_or_404(Caregiver, id=caregiver_id)

    # Fetch related notes
    notes = caregiver.notes.all()  # Use the related_name "notes" from the CaregiverNotes model

    # Define the pipeline stages in order
    stages = [
        PipelineStage.LEAD,
        PipelineStage.INTERVIEW_COMPLETED,
        PipelineStage.TRAINING_COMPLETED,
        PipelineStage.BACKGROUND_CHECKED,
        PipelineStage.READY_TO_WORK,
    ]

    # Get current stage index
    current_stage_index = stages.index(caregiver.stage)

    # Determine next and previous stages
    next_stage = stages[current_stage_index + 1] if current_stage_index + 1 < len(stages) else None
    previous_stage = stages[current_stage_index - 1] if current_stage_index > 0 else None

    next_action_label = f"Move to {next_stage}" if next_stage else None
    previous_action_label = f"Move to {previous_stage}" if previous_stage else None

    if request.method == "POST":
        caregiver.name = request.POST.get("name", caregiver.name)
        caregiver.age = request.POST.get("age", caregiver.age)
        caregiver.experience = request.POST.get("experience", caregiver.experience)
        caregiver.salary_expectation = request.POST.get("salary_expectation", caregiver.salary_expectation)
        caregiver.save()
        return redirect("caregiver_profile", caregiver_id=caregiver.id)

    return render(request, "recruitment/caregiver_profile.html", {
        "caregiver": caregiver,
        "notes": notes,  # Pass notes to the template
        "next_stage": next_stage,
        "next_action_label": next_action_label,
        "previous_stage": previous_stage,
        "previous_action_label": previous_action_label,
    })

# Move Backward in Stage
def move_backward_stage(request, caregiver_id):
    caregiver = get_object_or_404(Caregiver, id=caregiver_id)

    stages = [
        PipelineStage.LEAD,
        PipelineStage.INTERVIEW_COMPLETED,
        PipelineStage.TRAINING_COMPLETED,
        PipelineStage.BACKGROUND_CHECKED,
        PipelineStage.READY_TO_WORK,
    ]

    current_index = stages.index(caregiver.stage)
    if current_index > 0:
        caregiver.stage = stages[current_index - 1]
        caregiver.save()

    return redirect("caregiver_profile", caregiver_id=caregiver.id)

# Archive Caregiver
def archive_caregiver(request, caregiver_id):
    caregiver = get_object_or_404(Caregiver, id=caregiver_id)
    if request.method == "POST":
        caregiver.delete()
        return redirect("caregiver-pipeline")
    return JsonResponse({"error": "Invalid request method."}, status=405)

# Add notes
def add_notes(request, caregiver_id):
    caregiver = get_object_or_404(Caregiver, id=caregiver_id)
    if request.method == "POST":
        notes = request.POST.get("notes", "")
        file = request.FILES.get("files")

        # Save notes and files to the database or a file system
        # Example: Save notes to a hypothetical `CaregiverNotes` model
        if notes or file:
            CaregiverNotes.objects.create(caregiver=caregiver, notes=notes, file=file)

        return redirect("caregiver_profile", caregiver_id=caregiver.id)
    return JsonResponse({"error": "Invalid request method."}, status=405)
