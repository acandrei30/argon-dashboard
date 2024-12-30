from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from sales_pipeline.models import Lead
from datetime import datetime

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

def lead_profile(request, lead_id):
    """
    View to display the profile of a single lead.
    """
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == "POST":
        try:
            # Update lead details
            lead.name = request.POST.get("name", lead.name)
            lead.phone = request.POST.get("phone", lead.phone)
            lead.email = request.POST.get("email", lead.email)
            lead.location = request.POST.get("location", lead.location)
            lead.relation = request.POST.get("relation", lead.relation)
            lead.age = request.POST.get("age", lead.age)
            lead.medical_summary = request.POST.get("medical_summary", lead.medical_summary)
            lead.services_required = request.POST.get("services_required", lead.services_required)
            lead.save()

            return JsonResponse({"message": "Lead updated successfully!"}, status=200)

        except Exception as e:
            print("Error updating lead:", str(e))
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return render(request, "sales/lead_profile.html", {"lead": lead})
