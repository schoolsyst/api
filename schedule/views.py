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
    serializer_class = EventSerializer
    
class AdditionsViewSet(ModelViewSet):
    queryset = Addition.objects.all()
    serializer_class = AdditionSerializer
    
class DeletionsViewSet(ModelViewSet):
    queryset = Deletion.objects.all()
    serializer_class = DeletionSerializer

class ExercisesViewSet(ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    
class ComputedSchedule(ListAPIView):
    def get_queryset(self):
        
        # --- Get requested period ---
        # Get settings for user
        settings = Setting.objects.filter(user__pk=self.request.user.id)
        # Get request params and extract ?start and &end from url
        q = self.request.query_params
        q_period = [q.get('start', None), q.get('end', None)]
        # If any of the above query params are not specified, fall back to the settings values
        # (Get the entire schedule)
        if all([q is None for q in q_period]):
            q_period = [settings.get(name='schedule/start').value, settings.get(name='schedule/end').value]
        
        # --- Compute all dates for requested period ---
        # Turn dates into datetime objects
        to_date = lambda datestr: datetime.datetime.strptime(datestr, '%m/%d/%Y').date()
        dates = list(daterange(
            *[ to_date(datestr) for datestr in q_period ]
        ))
        
        # --- Get base events for each day---
        base_events = dict()
        weekday = lambda date: WEEK_DAYS[date.weekday()][0]
        for date in dates:
            print(weekday(date))
            base_events[date] = Event.objects.filter(day=weekday(date))
        
        print(base_events)
        
        
        
        return computed_events
    