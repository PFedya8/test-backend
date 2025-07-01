"""
URL Configuration for Task Service.

Defines the API endpoints for the task management system.
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tasks.views import TaskViewSet, healthz, readyz

# API Router configuration
router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz", healthz, name="health-check"),
    path("readyz", readyz, name="readiness-check"),
    path("", include(router.urls)),
]
