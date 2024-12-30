from django.urls import path
from . import views

urlpatterns = [
    path("pipeline/", views.sales_pipeline, name="sales-pipeline"),
    path("update/<int:lead_id>/<str:new_stage>/", views.update_stage, name="update-stage"),
    path('add_lead/', views.add_lead, name='add_lead'),
    path('lead/<int:lead_id>/', views.lead_profile, name='lead_profile'),
    path("archive/<int:lead_id>/", views.archive_lead, name="archive-lead"),
    path("lead/<int:lead_id>/move-backward/", views.move_backward_stage, name="move-backward-stage"),
    path('lead/<int:lead_id>/add-notes/', views.add_notes, name='add-notes'),
    path('sales-pipeline/update/<int:lead_id>/consultation/', views.update_lead_consultation, name='update-lead-consultation')
  
]
