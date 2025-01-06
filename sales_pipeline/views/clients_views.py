from django.shortcuts import render, get_object_or_404, redirect
from sales_pipeline.models import Lead
from django.utils.timezone import now


def clients(request):
    """
    View to display all clients.
    """
    # Filter leads with stage 'Active Client'
    clients = Lead.objects.filter(stage="Active Client").select_related("caregiver")

    # Add calculated client status for each client
    today = now().date()
    for client in clients:
        if client.start_date and client.start_date > today:
            client.client_status = f"To start on {client.start_date}"
        else:
            client.client_status = "Active"

    return render(request, "sales/clients.html", {
        "clients": clients,
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

        # Fetch caregiver if provided
        if caregiver_id:
            lead.caregiver_id = caregiver_id

        # Update lead details
        lead.start_date = start_date
        lead.end_date = end_date
        lead.days_per_week = days_per_week
        lead.hours_per_day = hours_per_day
        lead.price = price
        lead.caregiver_salary = caregiver_salary
        lead.additional_details = additional_details
        lead.stage = "Active Client"
        lead.save()

        # Redirect to the lead profile
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
