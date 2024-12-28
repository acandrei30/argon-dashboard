from django.urls import path
from . import views

urlpatterns = [
    path("pipeline/", views.caregiver_pipeline, name="caregiver-pipeline"),
   path('caregiver/update/<int:caregiver_id>/<str:new_stage>/', views.update_stage, name='caregiver-update-stage'),
    path('add_caregiver/', views.add_caregiver, name='add_caregiver'),
    path('caregiver/<int:caregiver_id>/', views.caregiver_profile, name='caregiver_profile'),
    path("archive/<int:caregiver_id>/", views.archive_caregiver, name="archive-caregiver"),
    path("caregiver/<int:caregiver_id>/move-backward/", views.move_backward_stage, name="move-backward-stage"),
    path('caregiver/<int:caregiver_id>/add-notes/', views.add_notes, name='add-notes'),
]
    
