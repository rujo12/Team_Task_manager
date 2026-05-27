from rest_framework.permissions import BasePermission
from utils.permissions import IsAdminRole


class IsTaskAssigneeOrAdmin(BasePermission):
    message = "Only the assigned user or an admin can update this task."

    def has_object_permission(self, request, view, obj):
        if request.user.role == "ADMIN":
            return True
        return obj.assigned_to_id == request.user.id
