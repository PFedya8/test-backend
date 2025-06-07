import logging
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.db import connections
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        logger.info("List tasks called", extra={"params": request.query_params.dict()})
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("Retrieve task", extra={"task_id": kwargs.get('pk')})
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info("Create task", extra={"data": request.data})
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info("Update task", extra={"task_id": kwargs.get('pk'), "data": request.data})
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info("Delete task", extra={"task_id": kwargs.get('pk')})
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        limit = self.request.query_params.get('limit')
        offset = self.request.query_params.get('offset')
        if offset:
            queryset = queryset[int(offset):]
        if limit:
            queryset = queryset[:int(limit)]
        return queryset

@api_view(['GET'])
def healthz(request):
    return HttpResponse('alive')

@api_view(['GET'])
def readyz(request):
    logger.info("Readyz check called - verifying database connection")
    try:
        connections['default'].cursor()
        logger.info("Database connection successful")
        return Response({'status': 'ok'})
    except OperationalError:
        logger.exception("Database connection failed")
        return Response({'status': 'error'}, status=500)
