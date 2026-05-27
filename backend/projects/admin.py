from django.contrib import admin
from .models import Project, ProjectMember


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Project admin."""
    
    list_display = ("name", "created_by", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "description", "created_by__username")
    readonly_fields = ("id", "created_at", "updated_at")
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ["created_by"]
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    """Project member admin."""
    
    list_display = ("get_project_name", "get_user_name", "role", "added_at")
    list_filter = ("role", "added_at")
    search_fields = ("project__name", "user__username", "user__email")
    readonly_fields = ("id", "added_at")
    
    def get_project_name(self, obj):
        return obj.project.name
    get_project_name.short_description = "Project"
    
    def get_user_name(self, obj):
        return obj.user.username
    get_user_name.short_description = "User"
