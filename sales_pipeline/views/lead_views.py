from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils.timezone import make_aware, get_current_timezone, is_aware  # Properly import get_current_timezone
from datetime import datetime, date, time
from sales_pipeline.models import Lead, LeadNotes, SalesPipelineStage
from django.utils.timezone import now  

def add_lead(request):
    """
    View to add a new lead.
    """
    if request.method == "POST":
        try:
            # Fetch data from the form
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            location = request.POST.get("location")
            relation = request.POST.get("relation")
            age = request.POST.get("age")
            medical_summary = request.POST.get("medical_summary")
            services_required = request.POST.get("services_required")
            follow_up_date = request.POST.get("follow_up_date")
            status = request.POST.get("status", "ready_for_consultation")  # Default to ready_for_consultation

            # Validate required fields
            if not name or not phone or not email:
                return JsonResponse({"error": "Name, phone, and email are required fields."}, status=400)

            # Conditional validation for follow-up date
            if status == "not_ready_for_consultation":
                if not follow_up_date:
                    return JsonResponse({"error": "Follow-up date is required for Not Ready for Consultation."}, status=400)

                try:
                    follow_up_date_parsed = datetime.strptime(follow_up_date, "%Y-%m-%d")
                except ValueError:
                    return JsonResponse({"error": "Invalid follow-up date format. Expected YYYY-MM-DD."}, status=400)
            else:
                follow_up_date_parsed = None  # Follow-up date is ignored for "Ready for Consultation"

            # Create the lead
            lead = Lead.objects.create(
                name=name,
                phone=phone,
                email=email,
                location=location,
                relation=relation,
                age=age if age else None,
                medical_summary=medical_summary,
                services_required=services_required,
                follow_up_date=follow_up_date_parsed,
                status=status,
            )

            return JsonResponse({"message": "Lead created successfully!"}, status=201)

        except Exception as e:
            print("Error while adding lead:", str(e))
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    return render(request, "sales/add_lead.html")

from django.shortcuts import render, get_object_or_404, redirect
from sales_pipeline.models import Lead, SalesPipelineStage

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from sales_pipeline.models import Lead, LeadNotes, SalesPipelineStage

def normalize_datetime(value):
    """
    Ensures the given value is a timezone-aware datetime object.
    Converts naive datetime or date objects into timezone-aware datetime.
    """
    if isinstance(value, datetime):  # Check for datetime
        return make_aware(value) if not is_aware(value) else value
    elif isinstance(value, date):  # Check for date
        return make_aware(datetime.combine(value, time.min), get_current_timezone())
    return None

def lead_profile(request, lead_id):
    """
    View to display the profile of a single lead.
    """
    lead = get_object_or_404(Lead, id=lead_id)

    # Fetch notes in reverse chronological order
    notes = lead.notes.order_by('-created_at')  # Assuming "notes" is the related_name for LeadNotes
    timeline = []  # Initialize timeline

    # Add notes to the timeline
    for note in notes:
        timeline.append({
            "type": "Note",
            "created_at": note.created_at,  # Use the note's creation time (already timezone-aware)
            "details": note.notes,  # Include note content
            "file": note.file.url if note.file else None,  # Include file if available
        })

    # Add consultation to the timeline
    if lead.consultation_datetime:
        consultation_creation_time = lead.consultation_creation_time or now()  # Ensure consultation event has a creation timestamp
        timeline.append({
            "type": "Consultation",
            "created_at": consultation_creation_time,  # Use actual creation timestamp
            "details": f"Consultation scheduled for {lead.consultation_datetime.strftime('%Y-%m-%d at %H:%M')}",  # Scheduled date in title
            "scheduled_date": lead.consultation_datetime,  # Include scheduled date for display
        })

    # Add follow-up to the timeline
    if lead.follow_up_date:
        follow_up_creation_time = lead.follow_up_creation_time or now()  # Ensure follow-up event has a creation timestamp
        timeline.append({
            "type": "Follow-Up",
            "created_at": follow_up_creation_time,  # Use actual creation timestamp
            "details": f"Follow-up scheduled for {lead.follow_up_date.strftime('%Y-%m-%d')}",  # Scheduled date in title
            "scheduled_date": normalize_datetime(datetime.combine(lead.follow_up_date, datetime.min.time())),  # Scheduled date for display
        })

    # Sort the timeline by created_at in descending order
    timeline = sorted(timeline, key=lambda x: x["created_at"], reverse=True)

    # Define pipeline stages in order
    stages = [
        SalesPipelineStage.PROSPECTING,
        SalesPipelineStage.CONSULTATION_SCHEDULED,
        SalesPipelineStage.UNDER_CONSIDERATION,
        SalesPipelineStage.CAREGIVER_INTERVIEW_SCHEDULED,
        SalesPipelineStage.CAREGIVER_CONSIDERATION,
        SalesPipelineStage.READY_FOR_SERVICE,
    ]

    # Get the current stage index and determine next/previous stages
    current_stage_index = stages.index(lead.stage) if lead.stage in stages else -1
    next_stage = stages[current_stage_index + 1] if current_stage_index + 1 < len(stages) else None
    previous_stage = stages[current_stage_index - 1] if current_stage_index > 0 else None

    next_action_label = f"Move to {next_stage}" if next_stage else None
    previous_action_label = f"Move to {previous_stage}" if previous_stage else None

    if request.method == "POST":
        try:
            # Update lead details
            lead.name = request.POST.get("name", lead.name).strip()
            lead.phone = request.POST.get("phone", lead.phone).strip()
            lead.email = request.POST.get("email", lead.email).strip()
            lead.location = request.POST.get("location", lead.location).strip()
            lead.relation = request.POST.get("relation", lead.relation).strip()
            lead.age = request.POST.get("age", lead.age)
            lead.medical_summary = request.POST.get("medical_summary", lead.medical_summary).strip()
            lead.services_required = request.POST.get("services_required", lead.services_required).strip()
            lead.save()

            return redirect("lead_profile", lead_id=lead.id)

        except Exception as e:
            print(f"Error updating lead: {e}")
            return JsonResponse({"error": f"An unexpected error occurred: {e}"}, status=500)

    return render(request, "sales/lead_profile.html", {
        "lead": lead,
        "timeline": timeline,  # Unified timeline for the template
        "next_stage": next_stage,
        "next_action_label": next_action_label,
        "previous_stage": previous_stage,
        "previous_action_label": previous_action_label,
    })