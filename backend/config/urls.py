"""URL configuration for Team Task Manager API."""

from django.contrib import admin
from django.urls import path, include
from users.views import CurrentUserView, LoginView, RefreshView, SignupView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/signup/", SignupView.as_view(), name="signup"),
    path("api/auth/login/", LoginView.as_view(), name="login"),
    path("api/auth/refresh/", RefreshView.as_view(), name="token_refresh"),
    path("api/auth/me/", CurrentUserView.as_view(), name="current_user"),
    path("api/users/", include("users.urls")),  # Legacy aliases
    path("api/projects/", include("projects.urls")),
    path("api/tasks/", include("tasks.urls")),
    path("api/dashboard/", include("dashboard.urls")),
]
