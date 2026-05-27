from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from .models import Task, TaskHistory
from .permissions import IsTaskAssigneeOrAdmin
from .serializers import TaskSerializer, TaskStatusUpdateSerializer
from utils.responses import error_response, success_response


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.select_related(
            "project",
            "assigned_to",
            "created_by",
        )
        if self.request.user.role == "ADMIN":
            return queryset
        return queryset.filter(assigned_to=self.request.user)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return success_response(data=serializer.data, http_status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if request.user.role != "ADMIN":
            return error_response(
                "Only admin users can create tasks.",
                error_code="permission_denied",
                http_status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(created_by=request.user)
        return success_response(
            data=self.get_serializer(task).data,
            http_status=status.HTTP_201_CREATED,
        )


class TaskStatusUpdateView(generics.GenericAPIView):
    serializer_class = TaskStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsTaskAssigneeOrAdmin]

    def patch(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        self.check_object_permissions(request, task)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_status = task.status
        task.status = serializer.validated_data["status"]
        task.save(update_fields=["status", "updated_at"])

        TaskHistory.objects.create(
            task=task,
            changed_by=request.user,
            field_changed="status",
            old_value=old_status,
            new_value=task.status,
        )

        return success_response(
            message="Task status updated.",
            data=TaskSerializer(task).data,
            http_status=status.HTTP_200_OK,
        )


class DashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Task.objects.all()
        if request.user.role != "ADMIN":
            queryset = queryset.filter(assigned_to=request.user)

        today = timezone.now().date()
        aggregates = queryset.aggregate(
            total_tasks=Count("id"),
            completed_tasks=Count("id", filter=Q(status="COMPLETED")),
            pending_tasks=Count("id", filter=~Q(status="COMPLETED")),
            overdue_tasks=Count(
                "id",
                filter=Q(due_date__lt=today) & ~Q(status="COMPLETED"),
            ),
        )

        return success_response(
            data=aggregates,
            http_status=status.HTTP_200_OK,
        )
