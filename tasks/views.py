from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.db import connections
from django.db.utils import OperationalError
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

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
    try:
        connections['default'].cursor()
        return Response({'status': 'ok'})
    except OperationalError:
        return Response({'status': 'error'}, status=500)
