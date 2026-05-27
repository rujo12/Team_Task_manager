from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class ProjectApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin_user", email="admin@example.com", password="StrongPass123", role="ADMIN"
        )
        self.member = User.objects.create_user(
            username="member_user", email="member@example.com", password="StrongPass123", role="MEMBER"
        )

    def authenticate(self, user):
        login_response = self.client.post(
            "/api/auth/login/",
            {"username": user.username, "password": "StrongPass123"},
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")

    def test_admin_can_create_project(self):
        self.authenticate(self.admin)
        response = self.client.post(
            "/api/projects/",
            {"name": "Website Revamp", "description": "Build new landing pages"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "success")

    def test_member_cannot_create_project(self):
        self.authenticate(self.member)
        response = self.client.post("/api/projects/", {"name": "Not Allowed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_add_member(self):
        self.authenticate(self.admin)
        project_response = self.client.post(
            "/api/projects/",
            {"name": "API Project", "description": ""},
            format="json",
        )
        project_id = project_response.data["data"]["id"]
        add_member_response = self.client.post(
            f"/api/projects/{project_id}/add-member/",
            {"user_id": self.member.id},
            format="json",
        )
        self.assertEqual(add_member_response.status_code, status.HTTP_201_CREATED)
