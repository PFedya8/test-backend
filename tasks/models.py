from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    """
    Task model representing a todo item with status tracking.
    """

    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]

    title = models.TextField(help_text="Task title or summary")
    description = models.TextField(
        blank=True, help_text="Detailed description of the task"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
        help_text="Current status of the task",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks",
        help_text="User assigned to this task",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def __repr__(self):
        return f"<Task: {self.id} - {self.title[:50]}>"
