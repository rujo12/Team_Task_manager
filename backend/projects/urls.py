"""
Project app URLs.

Endpoints for project management and member operations.
"""

from django.urls import path
from .views import ProjectListCreateView, AddProjectMemberView

app_name = "projects"

urlpatterns = [
    path("", ProjectListCreateView.as_view(), name="project-list-create"),
    path("<uuid:project_id>/add-member/", AddProjectMemberView.as_view(), name="project-add-member"),
]
