from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model with validation and custom field handling.
    """

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "user",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(self, value):
        """Validate that title is not empty or just whitespace."""
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()

    def validate_description(self, value):
        """Clean up description field."""
        return value.strip() if value else ""
