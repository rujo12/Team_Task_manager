"""
User views.

Views for user registration, login, and profile management.

API Endpoints:
- POST /api/auth/signup     - Register new user
- POST /api/auth/login      - Login and get JWT tokens
- POST /api/auth/refresh    - Refresh expired access token
- GET  /api/auth/me         - Get current user profile
"""

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import SignupSerializer, UserSerializer, CustomTokenObtainPairSerializer
from utils.responses import error_response, success_response


class SignupView(APIView):
    """
    User registration/signup endpoint.
    
    POST /api/auth/signup
    
    Creates a new user account with email and password.
    
    Request:
    {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "SecurePassword123",
        "confirm_password": "SecurePassword123",
        "role": "MEMBER",               (optional: ADMIN or MEMBER)
        "first_name": "John",              (optional)
        "last_name": "Doe"                 (optional)
    }
    
    Response (201 Created):
    {
        "status": "success",
        "message": "User registered successfully",
        "data": {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "username": "john_doe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "full_name": "John Doe",
            "date_joined": "2026-05-27T12:34:56Z"
        }
    }
    
    Response (400 Bad Request) - Validation Error:
    {
        "status": "error",
        "error": "validation_error",
        "message": "Validation failed",
        "details": {
            "username": ["This username is already taken."],
            "email": ["This email is already registered."],
            "password": ["Passwords do not match."]
        }
    }
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Register a new user."""
        serializer = SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return success_response(
                data=UserSerializer(user).data,
                message="User registered successfully. You can now login.",
                http_status=status.HTTP_201_CREATED,
            )
        
        return error_response(
            "User registration failed. Please check the details below.",
            details=serializer.errors,
            http_status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(TokenObtainPairView):
    """
    User login endpoint.
    
    POST /api/auth/login
    
    Authenticates user credentials and returns JWT tokens.
    
    Request:
    {
        "username": "john_doe",
        "password": "SecurePassword123"
    }
    
    Response (200 OK):
    {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user": {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "username": "john_doe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "full_name": "John Doe",
            "date_joined": "2026-05-27T12:34:56Z"
        }
    }
    
    Response (401 Unauthorized):
    {
        "detail": "No active account found with the given credentials."
    }
    
    Usage:
    - Store the 'access' token in Authorization header: "Bearer {access_token}"
    - When access token expires, use 'refresh' token at /api/auth/refresh/ endpoint
    """
    
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK and isinstance(response.data, dict):
            token_payload = response.data
            return Response(
                {
                    "status": "success",
                    "data": token_payload,
                    **token_payload,  # backward compatible top-level keys
                },
                status=status.HTTP_200_OK,
            )
        return response


class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK and isinstance(response.data, dict):
            refresh_payload = response.data
            return Response(
                {
                    "status": "success",
                    "data": refresh_payload,
                    **refresh_payload,  # backward compatible top-level keys
                },
                status=status.HTTP_200_OK,
            )
        return response


# Keep the old name for backwards compatibility
CustomTokenObtainPairView = LoginView


class CurrentUserView(APIView):
    """
    Get current authenticated user's profile.
    
    GET /api/auth/me
    
    Returns the profile of the currently authenticated user.
    
    Headers:
    Authorization: Bearer {access_token}
    
    Response (200 OK):
    {
        "status": "success",
        "data": {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "username": "john_doe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "full_name": "John Doe",
            "date_joined": "2026-05-27T12:34:56Z"
        }
    }
    
    Response (401 Unauthorized):
    {
        "detail": "Authentication credentials were not provided."
    }
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get current user profile."""
        serializer = UserSerializer(request.user)
        return success_response(
            data=serializer.data,
            http_status=status.HTTP_200_OK,
        )
