from django.contrib.auth import get_user_model
from rest_framework import serializers

from projects.models import ProjectMember
from .models import Task

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    is_overdue = serializers.BooleanField(read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)
    assigned_to_username = serializers.CharField(
        source="assigned_to.username",
        read_only=True,
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "project",
            "project_name",
            "title",
            "description",
            "assigned_to",
            "assigned_to_username",
            "status",
            "priority",
            "due_date",
            "is_overdue",
            "created_by",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_by",
            "created_at",
            "updated_at",
            "is_overdue",
        )

    def validate(self, attrs):
        project = attrs.get("project")
        assigned_to = attrs.get("assigned_to")

        if assigned_to and project:
            is_member = ProjectMember.objects.filter(
                project=project,
                user=assigned_to,
            ).exists()
            if not is_member:
                raise serializers.ValidationError(
                    {
                        "assigned_to": (
                            "Assigned user must be a member "
                            "of the selected project."
                        )
                    }
                )
        return attrs


class TaskStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)
