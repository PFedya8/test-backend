import logging

from django.db import connections
from django.db.utils import OperationalError
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer

logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Task objects with CRUD operations.
    Supports filtering by user_id and pagination via limit/offset.
    """

    queryset = Task.objects.all().order_by("-created_at")
    serializer_class = TaskSerializer

    def _log_action(self, action, **extra_data):
        """Helper method to log actions consistently."""
        logger.info(f"{action} task", extra=extra_data)

    def list(self, request, *args, **kwargs):
        self._log_action("List tasks", params=request.query_params.dict())
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self._log_action("Retrieve", task_id=kwargs.get("pk"))
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self._log_action("Create", data=request.data)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self._log_action("Update", task_id=kwargs.get("pk"), data=request.data)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self._log_action("Delete", task_id=kwargs.get("pk"))
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        """
        Filter queryset based on query parameters.
        Supports user_id filtering and pagination via limit/offset.
        """
        queryset = super().get_queryset()

        # Filter by user_id if provided
        user_id = self.request.query_params.get("user_id")
        if user_id:
            try:
                queryset = queryset.filter(user_id=int(user_id))
            except (ValueError, TypeError):
                logger.warning(f"Invalid user_id parameter: {user_id}")
                # Return empty queryset for invalid user_id
                return queryset.none()

        # Handle pagination parameters
        limit_param = self.request.query_params.get("limit")
        offset_param = self.request.query_params.get("offset")

        # Convert and validate limit parameter
        if limit_param:
            try:
                limit = int(limit_param)
                if limit < 0:
                    logger.warning(f"Invalid limit parameter: {limit}")
                    limit = None
            except (ValueError, TypeError):
                logger.warning(f"Invalid limit parameter: {limit_param}")
                limit = None
        else:
            limit = None

        # Convert and validate offset parameter
        if offset_param:
            try:
                offset = int(offset_param)
                if offset < 0:
                    logger.warning(f"Invalid offset parameter: {offset}")
                    offset = 0
            except (ValueError, TypeError):
                logger.warning(f"Invalid offset parameter: {offset_param}")
                offset = 0
        else:
            offset = 0

        # Apply database-level pagination for better performance
        if offset > 0:
            queryset = queryset[offset:]
        if limit is not None:
            queryset = queryset[:limit]

        return queryset


@api_view(["GET"])
def healthz(request):
    return HttpResponse("alive")


@api_view(["GET"])
def readyz(request):
    logger.info("Readyz check called - verifying database connection")
    try:
        connections["default"].cursor()
        logger.info("Database connection successful")
        return Response({"status": "ok"})
    except OperationalError:
        logger.exception("Database connection failed")
        return Response({"status": "error"}, status=500)
