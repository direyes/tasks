from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from app.models import Task
from app.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['description']
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.owner = self.request.user
        instance.save()

    def get_queryset(self):
        queryset = super(TaskViewSet, self).get_queryset()
        return queryset.filter(owner=self.request.user)
