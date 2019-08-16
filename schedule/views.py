from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.generics import ListAPIView
from .models import *
from common.models import Subject, Setting
from common.utils import daterange
from schedule.models import WEEK_DAYS
from .serializers import *
import datetime

class EventsViewSet(ModelViewSet):
    queryset = Event.objects.all()
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return EventReadSerialier
        return EventSerializer
    
class AdditionsViewSet(ModelViewSet):
    queryset = Addition.objects.all()
    serializer_class = AdditionSerializer
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return AdditionReadSerialier
        return AdditionSerializer
    
class DeletionsViewSet(ModelViewSet):
    queryset = Deletion.objects.all()
    serializer_class = DeletionSerializer
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return DeletionReadSerialier
        return DeletionSerializer

class ExercisesViewSet(ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ExerciseReadSerialier
        return ExerciseSerializer