from django.urls import path
from . import views

urlpatterns = [
    path("pipeline/", views.caregiver_pipeline, name="caregiver-pipeline"),
    path("add/", views.add_caregiver, name="add-caregiver"),
    path("update/<int:caregiver_id>/<str:new_stage>/", views.update_stage, name="update-stage"),
]
