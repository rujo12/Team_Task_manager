from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Project, ProjectMember

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    members_count = serializers.IntegerField(
        source="members.count",
        read_only=True,
    )

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description",
            "created_by",
            "members_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_by",
            "members_count",
            "created_at",
            "updated_at",
        )


class AddProjectMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist as exc:
            raise serializers.ValidationError("User does not exist.") from exc

        project = self.context["project"]
        if ProjectMember.objects.filter(project=project, user=user).exists():
            raise serializers.ValidationError(
                "User is already a member of this project."
            )
        return value

    def create(self, validated_data):
        project = self.context["project"]
        user = User.objects.get(id=validated_data["user_id"])
        return ProjectMember.objects.create(
            project=project,
            user=user,
            role="member",
        )
