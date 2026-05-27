"""
User app URLs.

Endpoints:
- /api/auth/signup       - POST - User registration
- /api/auth/login        - POST - User login (JWT)
- /api/auth/refresh      - POST - Refresh JWT token
- /api/users/me          - GET  - Get current user profile
"""

from django.urls import path
from .views import SignupView, CurrentUserView

app_name = "users"

urlpatterns = [
    # User registration
    path("signup/", SignupView.as_view(), name="user_signup"),
    
    # Get current user profile
    path("me/", CurrentUserView.as_view(), name="current_user"),
]
