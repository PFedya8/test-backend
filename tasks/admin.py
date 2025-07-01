from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin configuration for Task model with improved display and filtering.
    """

    list_display = ("title", "status", "user", "created_at", "updated_at")
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("title", "description", "user__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("title", "description", "status", "user")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
