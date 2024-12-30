from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Lead, SalesPipelineStage, LeadNotes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Lead  # Ensure Lead is imported

def sales_pipeline(request):
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
        stage: list(Lead.objects.filter(stage=stage).values("id", "name", "consultation_datetime"))
        for stage in stages.keys()
    }

    return render(request, "sales/pipeline.html", {
        "leads_by_stage": leads_by_stage,
        "stages": stages,
        "SalesPipelineStage": SalesPipelineStage,  # Pass constants to template
    })

# Add Lead
def add_lead(request):
    if request.method == "POST":
        # Get data from the form
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        location = request.POST.get("location")
        relation = request.POST.get("relation")
        age = request.POST.get("age")
        medical_summary = request.POST.get("medical_summary")
        services_required = request.POST.get("services_required")

        # Debug: Print the data to the console
        print("Received data:", name, phone, email, location, relation, age, medical_summary, services_required)
        
        # Create a new Lead object with the updated fields
        lead = Lead.objects.create(
            name=name,
            phone=phone,
            email=email,
            location=location,
            relation=relation,
            age=age if age else None,  # Handle optional age
            medical_summary=medical_summary,
            services_required=services_required,
        )

        # Debug: Check if lead was created
        print("Lead created:", lead)

        # Redirect to the sales pipeline after saving the lead
        return redirect("sales-pipeline")

    # Render the form template
    return render(request, "sales/add_lead.html")


# Update Lead Stage View
def update_stage(request, lead_id, new_stage):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == "POST" and new_stage in SalesPipelineStage.values:
        lead.stage = new_stage
        lead.save()
        return redirect("lead_profile", lead_id=lead.id)

    return JsonResponse({"error": "Invalid request."}, status=400)

# Lead Profile View
def lead_profile(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    # Fetch related notes
    notes = lead.notes.all()  # Use the related_name "notes" from the LeadNotes model

    # Define the pipeline stages in order
    stages = [
        SalesPipelineStage.PROSPECTING,
        SalesPipelineStage.CONSULTATION_SCHEDULED,
        SalesPipelineStage.UNDER_CONSIDERATION,
        SalesPipelineStage.CAREGIVER_INTERVIEW_SCHEDULED,
        SalesPipelineStage.CAREGIVER_CONSIDERATION,
        SalesPipelineStage.READY_FOR_SERVICE,
    ]

    # Get current stage index
    current_stage_index = stages.index(lead.stage)

    # Determine next and previous stages
    next_stage = stages[current_stage_index + 1] if current_stage_index + 1 < len(stages) else None
    previous_stage = stages[current_stage_index - 1] if current_stage_index > 0 else None

    next_action_label = f"Move to {next_stage}" if next_stage else None
    previous_action_label = f"Move to {previous_stage}" if previous_stage else None

    if request.method == "POST":
        lead.name = request.POST.get("name", lead.name)
        lead.company = request.POST.get("company", lead.company)
        lead.contact_info = request.POST.get("contact_info", lead.contact_info)
        lead.deal_value = request.POST.get("deal_value", lead.deal_value)
        lead.save()
        return redirect("lead_profile", lead_id=lead.id)

    return render(request, "sales/lead_profile.html", {
        "lead": lead,
        "notes": notes,  # Pass notes to the template
        "next_stage": next_stage,
        "next_action_label": next_action_label,
        "previous_stage": previous_stage,
        "previous_action_label": previous_action_label,
    })

# Move Backward in Stage
def move_backward_stage(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    stages = [
        SalesPipelineStage.PROSPECTING,
        SalesPipelineStage.CONSULTATION_SCHEDULED,
        SalesPipelineStage.UNDER_CONSIDERATION,
        SalesPipelineStage.CAREGIVER_INTERVIEW_SCHEDULED,
        SalesPipelineStage.CAREGIVER_CONSIDERATION,
        SalesPipelineStage.READY_FOR_SERVICE,
    ]

    current_index = stages.index(lead.stage)
    if current_index > 0:
        lead.stage = stages[current_index - 1]
        lead.save()

    return redirect("lead_profile", lead_id=lead.id)

# Archive Lead
def archive_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == "POST":
        lead.delete()
        return redirect("sales-pipeline")
    return JsonResponse({"error": "Invalid request method."}, status=405)

# Add notes
def add_notes(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == "POST":
        notes = request.POST.get("notes", "")
        file = request.FILES.get("files")

        # Save notes and files to the database or a file system
        if notes or file:
            LeadNotes.objects.create(lead=lead, notes=notes, file=file)

        return redirect("lead_profile", lead_id=lead.id)
    return JsonResponse({"error": "Invalid request method."}, status=405)

# Update Lead Consultation
# Update Lead Consultation View
def update_lead_consultation(request, lead_id):
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




