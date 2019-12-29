from drf_rw_serializers import generics
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


class LearndataViewSet(ModelViewSet):
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return LearndataReadSerializer
        return LearndataSerializer

    def get_queryset(self):
        user = self.request.user
        return Learndata.objects.filter(subject__user__id=user.id)


class NotesViewSet(ModelViewSet):
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return NoteReadSerializer
        return NoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(subject__user__id=user.id)
