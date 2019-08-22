from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.generics import ListAPIView
from .models import *
from common.models import Subject, Setting
from common.utils import daterange
from schedule.models import WEEK_DAYS
from .serializers import *
import datetime

class EventsViewSet(ModelViewSet):
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return EventReadSerializer
        return EventSerializer
    def get_queryset(self):
        user  = self.request.user
        return Event.objects.filter(subject__user__id=user.id)
    
class AdditionsViewSet(ModelViewSet):
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return AdditionReadSerializer
        return AdditionSerializer
    def get_queryset(self):
        user  = self.request.user
        return Addition.objects.filter(subject__user__id=user.id)


class DeletionsViewSet(ModelViewSet):
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return DeletionReadSerializer
        return DeletionSerializer
    def get_queryset(self):
        user  = self.request.user
        return Deletion.objects.filter(event__subject__user__id=user.id)
    

class ExercisesViewSet(ModelViewSet):
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ExerciseReadSerializer
        return ExerciseSerializer
    def get_queryset(self):
        user  = self.request.user
        return Exercise.objects.filter(subject__user__id=user.id)