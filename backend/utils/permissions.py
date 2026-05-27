from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """Allow access only to global ADMIN users."""

    message = "Only admin users can perform this action."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "ADMIN"
        )
