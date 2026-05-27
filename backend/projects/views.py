from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Project, ProjectMember
from .permissions import IsAdminRole
from .serializers import AddProjectMemberSerializer, ProjectSerializer
from utils.responses import error_response, success_response


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Project.objects.select_related("created_by").prefetch_related("members")
        if self.request.user.role == "ADMIN":
            return queryset
        return queryset.filter(members=self.request.user).distinct()

    def create(self, request, *args, **kwargs):
        if request.user.role != "ADMIN":
            return error_response(
                "Only admin users can create projects.",
                error_code="permission_denied",
                http_status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save(created_by=request.user)
        ProjectMember.objects.get_or_create(project=project, user=request.user, defaults={"role": "admin"})
        return success_response(
            data=self.get_serializer(project).data,
            http_status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return success_response(data=serializer.data, http_status=status.HTTP_200_OK)


class AddProjectMemberView(generics.GenericAPIView):
    serializer_class = AddProjectMemberSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        serializer = self.get_serializer(data=request.data, context={"project": project})
        serializer.is_valid(raise_exception=True)
        membership = serializer.save()
        return success_response(
            message="Member added successfully.",
            data={
                "project_id": str(project.id),
                "user_id": membership.user.id,
                "username": membership.user.username,
            },
            http_status=status.HTTP_201_CREATED,
        )
