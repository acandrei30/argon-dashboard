from django.urls import path
from . import views

urlpatterns = [
    path("", views.sales_pipeline, name="sales-pipeline"),
    path("add-lead/", views.add_lead, name="add-lead"),
    path("lead/<int:lead_id>/", views.lead_profile, name="lead-profile"),
]
