from django.contrib import admin
from .models import Task, TaskHistory


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Task admin."""
    
    list_display = ("title", "project", "assigned_to", "status", "priority", "due_date", "is_overdue")
    list_filter = ("status", "priority", "due_date", "created_at")
    search_fields = ("title", "description", "project__name", "assigned_to__username")
    readonly_fields = ("id", "created_at", "updated_at", "is_overdue")
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("project", "title", "description")
        }),
        ("Assignment", {
            "fields": ("assigned_to", "created_by")
        }),
        ("Status", {
            "fields": ("status", "priority", "due_date", "is_overdue")
        }),
        ("Dates", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ["created_by"]
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(TaskHistory)
class TaskHistoryAdmin(admin.ModelAdmin):
    """Task history admin."""
    
    list_display = ("task", "field_changed", "changed_by", "changed_at")
    list_filter = ("field_changed", "changed_at")
    search_fields = ("task__title", "changed_by__username")
    readonly_fields = ("id", "task", "changed_by", "field_changed", "old_value", "new_value", "changed_at")
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
