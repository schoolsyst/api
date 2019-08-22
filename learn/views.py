from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


class NotesViewSet(ModelViewSet):
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return NoteReadSerializer
        return NoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(subject__user__id=user.id)


class TestsViewSet(ModelViewSet):
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return TestReadSerializer
        return TestSerializer

    def get_queryset(self):
        user = self.request.user
        return Test.objects.prefetch_related('notes__subject__user').filter(
            id=user.id)


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
