"""
Task models.

Models for task management and task history tracking.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()


class Task(models.Model):
    """
    Task model for organizing work items.
    
    Fields:
        - id: UUID primary key
        - project: Project this task belongs to
        - title: Task title
        - description: Task description
        - assigned_to: User assigned to this task
        - status: Current status (todo, in_progress, completed)
        - priority: Task priority (low, medium, high)
        - due_date: Task due date
        - created_by: User who created the task
        - created_at: Creation timestamp
        - updated_at: Last update timestamp
    """
    
    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]
    
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="tasks",
        help_text="Project this task belongs to"
    )
    title = models.CharField(max_length=255, help_text="Task title")
    description = models.TextField(blank=True, help_text="Task description")
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
        help_text="User assigned to this task"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="TODO",
        help_text="Current task status"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium",
        help_text="Task priority"
    )
    due_date = models.DateField(null=True, blank=True, help_text="Due date")
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks_created",
        help_text="User who created this task"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["project", "status"]),
            models.Index(fields=["assigned_to"]),
            models.Index(fields=["created_at"]),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def is_overdue(self):
        """Check if task is overdue."""
        if self.due_date and self.status != "COMPLETED":
            return self.due_date < timezone.now().date()
        return False


class TaskHistory(models.Model):
    """
    TaskHistory model for tracking changes to tasks.
    
    Fields:
        - task: Task reference
        - changed_by: User who made the change
        - field_changed: Name of field that changed
        - old_value: Previous value
        - new_value: New value
        - changed_at: When change was made
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="history"
    )
    changed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="task_changes"
    )
    field_changed = models.CharField(
        max_length=50,
        help_text="Name of field that changed"
    )
    old_value = models.CharField(
        max_length=255,
        blank=True,
        help_text="Previous value"
    )
    new_value = models.CharField(
        max_length=255,
        blank=True,
        help_text="New value"
    )
    changed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-changed_at"]
        indexes = [
            models.Index(fields=["task", "changed_at"]),
        ]
    
    def __str__(self):
        return f"{self.task.title} - {self.field_changed} changed by {self.changed_by.username}"
