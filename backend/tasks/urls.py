"""
Task app URLs.

Endpoints for task management and status updates.
"""

from django.urls import path
from .views import TaskListCreateView, TaskStatusUpdateView

app_name = "tasks"

urlpatterns = [
    path("", TaskListCreateView.as_view(), name="task-list-create"),
    path("<uuid:task_id>/status/", TaskStatusUpdateView.as_view(), name="task-status-update"),
]
