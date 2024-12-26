from django.urls import path
from . import views

urlpatterns = [
    path("pipeline/", views.caregiver_pipeline, name="caregiver-pipeline"),
    path("update/<int:caregiver_id>/<str:new_stage>/", views.update_stage, name="update-stage"),
    path('add_caregiver/', views.add_caregiver, name='add_caregiver'),
    path('caregiver/<int:caregiver_id>/', views.caregiver_profile, name='caregiver_profile'),
    
]
