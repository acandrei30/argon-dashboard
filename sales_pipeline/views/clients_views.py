from django.shortcuts import render, get_object_or_404, redirect
from sales_pipeline.models import Lead
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime

def clients(request):
    """
    View to display all clients.
    """
    # Filter leads in the 'Active Client' stage only
    clients = Lead.objects.filter(stage="Active Client").select_related("caregiver")

    # Add calculated client status dynamically
    today = now().date()
    for client in clients:
        if client.start_date and client.start_date > today:
            client.client_status = f"To start on {client.start_date.strftime('%Y-%m-%d')}"
        else:
            client.client_status = "Active"

    return render(request, "sales/clients.html", {
        "clients": clients,  # Pass the clients to the template
        "today": today,      # Pass today's date for template logic
    })

def mark_ready_to_service(request, lead_id):
    """
    Mark a lead as Ready to Service, transitioning them to the Active Client stage.
    """
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        days_per_week = request.POST.get("days_per_week")
        hours_per_day = request.POST.get("hours_per_day")
        price = request.POST.get("price")
        caregiver_salary = request.POST.get("caregiver_salary")
        caregiver_id = request.POST.get("caregiver_id")  # Get the selected caregiver
        additional_details = request.POST.get("additional_details")

        try:
            # Validate and parse start_date
            if not start_date:
                raise ValidationError("Start date is required.")
            lead.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

            # Validate and parse end_date (if provided)
            if end_date:
                parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                if parsed_end_date < lead.start_date:
                    raise ValidationError("End date cannot be before start date.")
                lead.end_date = parsed_end_date
            else:
                lead.end_date = None  # Set to None for "undetermined" service type

            # Validate and update days per week
            if not days_per_week or int(days_per_week) <= 0:
                raise ValidationError("Days per week must be a positive number.")
            lead.days_per_week = int(days_per_week)

            # Validate and update hours per day
            if not hours_per_day or int(hours_per_day) <= 0:
                raise ValidationError("Hours per day must be a positive number.")
            lead.hours_per_day = int(hours_per_day)

            # Validate and update price
            if not price or float(price) <= 0:
                raise ValidationError("Price must be a positive number.")
            lead.price = float(price)

            # Validate and update caregiver salary
            if not caregiver_salary or float(caregiver_salary) <= 0:
                raise ValidationError("Caregiver salary must be a positive number.")
            lead.caregiver_salary = float(caregiver_salary)

            # Update caregiver if provided
            if caregiver_id:
                lead.caregiver_id = caregiver_id

            # Update additional details
            lead.additional_details = additional_details

            # Transition the lead to "Active Client"
            lead.stage = "Active Client"
            lead.save()

            # Redirect to the lead profile
            return redirect("lead_profile", lead_id=lead.id)

        except ValidationError as e:
            # Handle validation errors and return an appropriate response
            return redirect("lead_profile", lead_id=lead.id, error=str(e))
    else:
        return redirect("lead_profile", lead_id=lead.id)


def client_profile(request, client_id):
    """
    Displays the profile of a specific client.
    """
    client = get_object_or_404(Lead, id=client_id, stage="Active Client")

    return render(request, "sales/client_profile.html", {
        "client": client,
    })


def archive_client(request, client_id):
    """
    Archives a client, transitioning them out of the Active Client stage.
    """
    client = get_object_or_404(Lead, id=client_id, stage="Active Client")

    if request.method == "POST":
        # Update the stage and status
        client.stage = "Archived"
        client.status = "Archived"
        client.save()

        # Redirect back to the Clients page
        return redirect("clients")

    return redirect("client_profile", client_id=client.id)

def save_service_details(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    
    if request.method == "POST":
        try:
            lead.start_date = request.POST.get("start_date")
            lead.end_date = request.POST.get("end_date") if request.POST.get("service_type") == "short-term" else None
            lead.days_per_week = request.POST.get("days_per_week")
            lead.hours_per_day = request.POST.get("hours_per_day")
            lead.price = request.POST.get("price")
            lead.caregiver_salary = request.POST.get("caregiver_salary")
            lead.additional_details = request.POST.get("additional_details")
            caregiver_id = request.POST.get("caregiver_id")
            
            if caregiver_id:
                lead.caregiver_id = caregiver_id

            lead.save()
            return redirect("lead_profile", lead_id=lead.id)
        except Exception as e:
            print(f"Error updating service details: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "sales/service_details.html", {"lead": lead})
