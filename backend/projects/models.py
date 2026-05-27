"""
Project models.

Models for project and project member management.
"""

from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Project(models.Model):
    """
    Project model for organizing tasks.
    
    Fields:
        - id: UUID primary key
        - name: Project name
        - description: Project description
        - created_by: User who created the project
        - members: Team members (M2M through ProjectMember)
        - created_at: Creation timestamp
        - updated_at: Last update timestamp
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Project name")
    description = models.TextField(blank=True, help_text="Project description")
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="projects_created",
        help_text="User who created this project"
    )
    members = models.ManyToManyField(
        User,
        through="ProjectMember",
        related_name="projects",
        help_text="Team members in this project"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_by"]),
            models.Index(fields=["created_at"]),
        ]
    
    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    """
    Project member model (join table for Project-User relationship).
    
    Fields:
        - project: Project reference
        - user: User reference
        - role: User role in project (admin or member)
        - added_at: When user was added to project
    """
    
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("member", "Member"),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project_members"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="project_memberships"
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="member",
        help_text="Role of user in project"
    )
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("project", "user")
        ordering = ["-added_at"]
    
    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.role})"
    
    def is_admin(self):
        """Check if user is admin in this project."""
        return self.role == "admin"
    
    def is_member(self):
        """Check if user is regular member in this project."""
        return self.role == "member"
