from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


class HomeworkViewSet(ModelViewSet):
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return HomeworkReadSerializer
        return Homeworkerializer

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
        # Thanks django for this
        return Grade.objects.prefetch_related(
            'test__notes__subject__user').filter(id=user.id)
