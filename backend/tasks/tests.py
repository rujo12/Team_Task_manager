from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from projects.models import Project, ProjectMember
from tasks.models import Task
from users.models import User


class TaskAndDashboardApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin_user",
            email="admin@example.com",
            password="StrongPass123",
            role="ADMIN",
        )
        self.member = User.objects.create_user(
            username="member_user",
            email="member@example.com",
            password="StrongPass123",
            role="MEMBER",
        )
        self.project = Project.objects.create(
            name="Core Platform",
            description="Main build",
            created_by=self.admin,
        )
        ProjectMember.objects.create(
            project=self.project,
            user=self.admin,
            role="admin",
        )
        ProjectMember.objects.create(
            project=self.project,
            user=self.member,
            role="member",
        )

    def authenticate(self, user):
        login_response = self.client.post(
            "/api/auth/login/",
            {"username": user.username, "password": "StrongPass123"},
            format="json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}"
        )

    def test_admin_can_create_task(self):
        self.authenticate(self.admin)
        response = self.client.post(
            "/api/tasks/",
            {
                "project": str(self.project.id),
                "title": "Implement endpoint",
                "description": "Create task endpoint",
                "assigned_to": self.member.id,
                "status": "TODO",
                "priority": "high",
                "due_date": str(timezone.now().date() + timedelta(days=2)),
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_member_can_update_own_task_status(self):
        task = Task.objects.create(
            project=self.project,
            title="Member task",
            description="",
            assigned_to=self.member,
            status="TODO",
            created_by=self.admin,
        )
        self.authenticate(self.member)
        response = self.client.patch(
            f"/api/tasks/{task.id}/status/",
            {"status": "IN_PROGRESS"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, "IN_PROGRESS")

    def test_dashboard_returns_metrics(self):
        Task.objects.create(
            project=self.project,
            title="Done task",
            assigned_to=self.member,
            status="COMPLETED",
            created_by=self.admin,
        )
        Task.objects.create(
            project=self.project,
            title="Overdue task",
            assigned_to=self.member,
            status="TODO",
            due_date=timezone.now().date() - timedelta(days=1),
            created_by=self.admin,
        )

        self.authenticate(self.member)
        response = self.client.get("/api/dashboard/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["total_tasks"], 2)
        self.assertEqual(response.data["data"]["completed_tasks"], 1)
        self.assertEqual(response.data["data"]["overdue_tasks"], 1)
