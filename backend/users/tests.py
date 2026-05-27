from rest_framework import status
from rest_framework.test import APITestCase

class AuthApiTests(APITestCase):
    def test_signup_login_and_me_flow(self):
        signup_response = self.client.post(
            "/api/auth/signup/",
            {
                "username": "member_user",
                "email": "member@example.com",
                "password": "StrongPass123",
                "password_confirm": "StrongPass123",
            },
            format="json",
        )
        self.assertEqual(signup_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(signup_response.data["status"], "success")

        login_response = self.client.post(
            "/api/auth/login/",
            {"username": "member_user", "password": "StrongPass123"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access_token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        me_response = self.client.get("/api/auth/me/")
        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        self.assertEqual(me_response.data["data"]["username"], "member_user")

    def test_signup_password_confirmation_validation(self):
        response = self.client.post(
            "/api/auth/signup/",
            {
                "username": "wrong_confirm",
                "email": "wrong@example.com",
                "password": "StrongPass123",
                "password_confirm": "StrongPass124",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "error")
