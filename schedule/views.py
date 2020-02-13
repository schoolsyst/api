from django.db.models import Q
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from common.models import Subject, Setting
from common.utils import daterange, date_in_range, dateranges_overlap
from schedule.models import WEEK_DAYS
from .serializers import *
import datetime
import dateutil

class EventsViewSet(ModelViewSet):
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return EventReadSerializer
        return EventSerializer
    def get_queryset(self):
        user  = self.request.user
        return Event.objects.filter(subject__user__id=user.id)

    @action(methods=['get'], detail=False)
    def courses(self, request, start, end):
        """
        /courses/:start/:end

        QUERY PARAMS
        ------------
        include: ','-separated list of 'deleted', 'added', 'rescheduled', 'offdays'
            Choose what types of mutation-affected course to show.
            Unaffected courses are always included.
            Courses are marked as such with the `mutation` attribute
            Default: added,rescheduled,deleted

        week-type: ','-separated list of 'Q1', 'Q2' | 'auto'
            Choose which week types to include.
            'auto': only shows the current week type.
            Default: Q1
        
        TODO(beta-1.1.0): handle /courses/:start
        TODO(beta-1.1.0): handle ?week-type=auto
        MAYBE(beta-1.1.0): use ?start & ?end instead of url fragments
        """
        user = request.user
        #
        # Query params processing
        #

        # Get the date format and parse accordingly
        def parse_iso8601(value):
            fmt = 'datetime' if 'T' in value else 'date'
            if '/' in value:
                value = datetime.datetime.strptime(value, '%d/%m/%Y')
            else:
                value = datetime.datetime.fromisoformat(value)
            return (fmt, value)
        
        # Processing start & end
        start_fmt, start = parse_iso8601(start)
        end_fmt, end = parse_iso8601(end)
        if start_fmt != end_fmt:
            return Response({
                'error': 'Date range bounds must have the same format',
            })
        
        using_time = start_fmt == 'datetime' # We could have picked end_fmt since start_fmt == end_fmt

        # Processing include
        include = request.query_params.get('include', 'added,rescheduled,deleted')
        include = [ i.strip() for i in include.split(',') ]
        # Translating query parameter's mutation types into internal ones used by .models.Mutation 
        mutation_types_map = {
            'deleted': 'DEL',
            'rescheduled': 'RES',
            'added': 'ADD'
        }
        include = [ mutation_types_map.get(i, i) for i in include ]

        # Processing week-type
        week_types = request.query_params.get('week-type', 'Q1')
        week_types = [ w.strip() for w in week_types.split(',') ]

        #
        # Additionnal data processing
        #

        # Getting offdays as date ranges
        # Get the raw setting
        try:
            offdays = Setting.objects.get(setting__key='offdays').value
        except Setting.DoesNotExist:
            offdays = []
        else:
            # Each line is a new daterange/date
            offdays = offdays.split('\n')
            # Split to get start & end
            offdays = [ o.split(' - ') for o in offdays ]
            # For simple dates, set start & end to the same date
            offdays = [ [d[0], d[0]] for d in offdays if len(d) == 1 ]
            # Parse the offdays' start & end dates into datetime.date objects
            offdays = [ 
                [ parse_iso8601(d.strip())[1] for d in o ]
                for o in offdays
            ]

        #
        # Collecting events
        #

        # Init the variable containing all the courses
        courses = []

        # Loop over each day of the range
        for day in daterange(start, end):
            # TODO: handle ADD mutations
            # Get the relevant events
            events = Event.objects.filter(
                Q(week_type__in=week_types) | Q(week_type='BOTH'),
                Q(day=int(day.strftime('%u'))),
                Q(subject__user__id=user.id)
            )
            # Set the date part of each event, instead of a HH:MM time. (for start & end)
            for event in events:
                # Combine the date parts and the time parts
                event.start = datetime.datetime.combine(
                    day.date(), # The loop's day (date part)
                    event.start # The event's start time (time part)
                )
                # Do the same for the end
                event.end = datetime.datetime.combine(
                    day.date(),
                    event.end
                )

                # Check if the event is in offdays
                event.is_offday = False
                # For each offday daterange
                for offday in offdays:
                    offday_start, offday_end = offday
                    # Check if the event is in it
                    # If its already an offday because of another offday daterange, no need to check.
                    if not event.is_offday:
                        event.is_offday = dateranges_overlap(
                            (event.start,  event.end), 
                            (offday_start, offday_end)
                        )

                # Don't add the course to the list if the conditions aren't met
                if event.is_offday and 'offdays' not in include:
                    continue

                # Check if the event matches a mutation
                # (for EDT/RES/DEL mutations)
                # for ADD mutations, the mutation isn't bounded to an event.
                # We treat this separetly, and add them to the courses list outside of the events loop
                event.mutation = None
                for mutation in event.mutations.all():
                    # Determine if the mutation's date ranges matches the event
                    deleted_matches = False
                    added_matches = False
                    # Mutation types: see models.Mutation
                    if mutation.type in ('DEL', 'RES'):
                        deleted_matches = dateranges_overlap(
                            (mutation.deleted_start, mutation.deleted_end),
                            (event.start, event.end)
                        )
                    elif mutation.type == 'RES':
                        added_matches = dateranges_overlap(
                            (mutation.added_start, mutation.added_end),
                            (event.start, event.end)
                        )
                    # There should be at most one mutation relating to a single _course_ (not event).
                    # We set the mutation without further checking.
                    event.mutation = mutation

                event.original_room = event.room
                if event.mutation is not None:
                    # Process EDT/RES mutations that could modify the room
                    if event.mutation.type in ('EDT', 'RES') and event.mutation.room is not None:
                        event.room = event.mutation.room
                
                    # Don't append courses whose mutation's type is not in include
                    if event.mutation.type not in include:
                        continue
                # Append the course to the list
                courses.append(event)

        # Return the response
        return Response([ CourseReadSerializer(course).data for course in courses ])

class MutationsViewSet(ModelViewSet):
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return MutationReadSerializer
        return MutationSerializer
    def get_queryset(self):
        user  = self.request.user
        return Mutation.objects.filter(event__subject__user__id=user.id)
