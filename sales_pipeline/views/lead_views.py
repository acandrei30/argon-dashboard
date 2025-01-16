from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils.timezone import make_aware, get_current_timezone, is_aware  # Properly import get_current_timezone
from datetime import datetime, date, time
from sales_pipeline.models import Lead, LeadNotes, SalesPipelineStage
from django.utils.timezone import now  
from recruitment.models import Caregiver, PipelineStage  # Import Caregiver model
from django.db.models import Q
from django.db import transaction, IntegrityError

from django.db import transaction, IntegrityError
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render

def add_lead(request):
    """
    View to add a new lead.
    """
    if request.method == "POST":
        try:
            with transaction.atomic():
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
                status = request.POST.get("status", "ready_for_consultation")  # Default

                # Validate required fields
                if not name or not phone or not email:
                    return JsonResponse({"error": "Name, phone, and email are required fields."}, status=400)

                # Validate follow-up date
                if status == "not_ready_for_consultation":
                    if not follow_up_date:
                        return JsonResponse({"error": "Follow-up date is required."}, status=400)
                    follow_up_date_parsed = datetime.strptime(follow_up_date, "%Y-%m-%d")
                else:
                    follow_up_date_parsed = None

                # Check if lead already exists
                existing_lead = Lead.objects.filter(
                    name=name,
                    phone=phone,
                    email=email,
                    status=status
                ).first()

                if existing_lead:
                    # Update follow-up details if it's a "Not Ready for Consultation" case
                    if status == "not_ready_for_consultation":
                        existing_lead.follow_up_date = follow_up_date_parsed
                        existing_lead.save()
                        return JsonResponse({"message": "Follow-up updated successfully!"}, status=200)

                    return JsonResponse({"lead_id": existing_lead.id}, status=200)

                # Create lead if not existing
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

                return JsonResponse({"message": "Lead created successfully!", "lead_id": lead.id}, status=201)

        except IntegrityError:
            return JsonResponse({"error": "An unexpected error occurred. Please try again."}, status=500)
        except Exception as e:
            print("Error while adding lead:", str(e))
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    return render(request, "sales/add_lead.html")


from django.shortcuts import render, get_object_or_404, redirect
from sales_pipeline.models import Lead, SalesPipelineStage

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from sales_pipeline.models import Lead, LeadNotes, SalesPipelineStage

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now, is_aware, make_aware
from datetime import datetime, date, time
from sales_pipeline.models import Lead, LeadNotes, SalesPipelineStage

def normalize_datetime(value):
    """
    Normalize datetime to ensure it's timezone-aware.
    """
    if isinstance(value, datetime):
        return value if is_aware(value) else make_aware(value)
    return None

def lead_profile(request, lead_id):
    """
    View to display the profile of a single lead.
    """
    lead = get_object_or_404(Lead, id=lead_id)
    consultation = getattr(lead, 'consultation', None)  # Fetch consultation if it exists
    caregivers = Caregiver.objects.all()

    # Fetch notes in reverse chronological order
    notes = lead.notes.order_by('-created_at')  # Assuming "notes" is the related_name for LeadNotes
    timeline = []  # Initialize timeline

    # Add notes to the timeline
    for note in notes:
        timeline.append({
            "type": "Note",
            "created_at": normalize_datetime(note.created_at),  # Normalize datetime
            "details": note.notes,
            "file": note.file.url if note.file else None,
        })

    # Add consultation details to the timeline
    if consultation:
        consultation_data = [
            f"Alertness: {consultation.alertness}",
            f"Lives Alone: {consultation.lives_alone}",
            f"House Suitable: {consultation.house_suitable}",
            f"Speech Impairment: {consultation.speech_impairment}",
            f"Sight Impairment: {consultation.sight_impairment}",
            f"Hearing Impairment: {consultation.hearing_impairment}",
            f"Locomotive Impairment: {consultation.locomotive_impairment}",
            f"Lifting Required: {consultation.lifting_required}",
            f"Personal Help: {consultation.personal_help}",
            f"Allergies: {consultation.allergies or 'None'}",
            f"Recent Hospitalization: {consultation.recent_hospitalization}",
            f"Hospitalization Reason: {consultation.hospitalization_reason or 'None'}",
        ]
        timeline.append({
            "type": "Consultation",
            "created_at": now(),
            "details": " | ".join(consultation_data),
        })

    # Add consultation scheduling to the timeline
    if lead.consultation_datetime:
        consultation_creation_time = lead.consultation_creation_time or now()
        timeline.append({
            "type": "Consultation Scheduled",
            "created_at": normalize_datetime(consultation_creation_time),
            "details": f"Consultation scheduled for {lead.consultation_datetime.strftime('%Y-%m-%d %H:%M')}",
            "scheduled_date": normalize_datetime(lead.consultation_datetime),
        })

    # Add follow-up to the timeline
    if lead.follow_up_date:
        follow_up_creation_time = lead.follow_up_creation_time or now()
        timeline.append({
            "type": "Follow-Up",
            "created_at": normalize_datetime(follow_up_creation_time),
            "details": f"Follow-up scheduled for {lead.follow_up_date.strftime('%Y-%m-%d')}",
            "scheduled_date": normalize_datetime(datetime.combine(lead.follow_up_date, time.min)),
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

    return render(request, "sales/lead_profile.html", {
        "lead": lead,
        "consultation": consultation,
        "timeline": timeline,  # Unified timeline for the template
        "next_stage": next_stage,
        "next_action_label": next_action_label,
        "previous_stage": previous_stage,
        "previous_action_label": previous_action_label,
        "caregivers": caregivers,
    })

def consultation_options(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    return render(request, "sales/consultation_options.html", {"lead_id": lead_id})
