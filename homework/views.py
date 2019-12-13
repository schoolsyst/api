from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


class HomeworkViewSet(ModelViewSet):
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return HomeworkReadSerializer
        return HomeworkSerializer

    def get_queryset(self):
        user = self.request.user
        return Homework.objects.filter(subject__user__id=user.id)


class GradesViewSet(ModelViewSet):
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return GradeReadSerializer
        return GradeSerializer

    def get_queryset(self):
        user = self.request.user
        return Grade.objects.filter(subject__user__id=user.id)