from django.utils.translation import gettext as _
from django.db.models import *
import uuid

WEEK_DAYS = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
]

WEEK_TYPES = [
    ('BOTH', 'Both'),
    ('Q1', 'Q1'),
    ('Q2', 'Q2'),
]


# Create your models here.
class Event(Model):
    subject = ForeignKey(to='common.Subject',
                         related_name='events',
                         on_delete=CASCADE)
    uuid = UUIDField("UUID",
                     default=uuid.uuid4,
                     editable=False,
                     unique=True)
    #mutations (M2M relationship stored in Mutation)

    start = TimeField()
    end = TimeField()
    room = CharField(max_length=300, blank=True, null=True)
    day = IntegerField(choices=WEEK_DAYS)
    week_type = CharField(choices=WEEK_TYPES,
                          max_length=max([len(e[0]) for e in WEEK_TYPES]),
                          default=WEEK_TYPES[0])

    def __str__(self):
        return "{user}: {subject:.3} @ {week_type:^2} {day_word:.3} {start}--{end}"\
            .format(
                user=self.subject.user.username,
                subject=self.subject.name, 
                start=self.start, 
                end=self.end, 
                day_word=WEEK_DAYS[self.day-1][1],
                week_type=self.week_type if self.week_type != 'BOTH' else ''
            )

class Mutation(Model):
    """
    Represents schedule mutations.
    Multiple interpretations occur following which values are 
    taken by added & rescheduled's start and end dates 
    (_start & _end for both added & rescheduled)
    
    A := added_start    is not None   and added_end   is not None
    D := deleted_start  is not None   and deleted_end is not None
    S := added_start == deleted_start and added_end == deleted_end

       |  A && D   | A && !D	| !A && D	| !A && !D
    --------------------------------------------------
    S  | EDT	   | Ø   	    | Ø 	    | Ø
    !S | RES	   | ADD	    | DEL	    | Ø

    EDT: The mutation represents a simple editing of the course,
         while keeping it on the same day. 
         Example: for the 2019-12-08 Physics course from 08:00 to 08:55, 
                  the room is L013 and not L453
    
    RES: The mutation represents a rescheduling. 
         The room and other info may also be changed
         for the rescheduled event.
         Example: the 2019-08-12 Mathematics course from 13:05 to 14:00
                  is moved to 2019-08-14 from 08:00 to 08:55
    
    ADD: The mutation represents an exceptional course 
         that is not part of the regular schedule.
         Example: an exceptional History course will be added 
                  at 2019-07-11, from 16:45 to 18:00
    
    DEL: The mutation represents a removal of course, without rescheduling.
         Example: the 2020-01-13 Chemistry course from 15:50 to 16:45
                  is cancelled
    """
    event = ForeignKey(to='schedule.Event',
                       related_name='mutations',
                       on_delete=SET_NULL,
                       blank=True,
                       null=True)
    subject = ForeignKey(to='common.Subject', 
                         related_name='mutations',
                         on_delete=CASCADE)
    uuid = UUIDField("UUID",
                     default=uuid.uuid4,
                     editable=False,
                     unique=True)
    # Dates
    deleted_start = DateTimeField(blank=True, null=True)
    deleted_end = DateTimeField(blank=True, null=True)

    added_start = DateTimeField(blank=True, null=True)
    added_end = DateTimeField(blank=True, null=True)
    # Other info
    room = CharField(max_length=300,
                     blank=True,
                     null=True)
    
    # In the docstring's table: S
    def deleted_same_as_added(self):
        return self.deleted_start == self.added_start \
           and self.deleted_end   == self.added_end

    # In the docstring's table: A
    def added(self):
        return self.added_start is not None \
           and self.added_end   is not None \

    # In the docstring's table: D
    def deleted(self):
        return self.deleted_start is not None \
           and self.deleted_end   is not None

    @property
    def type(self):
        if self.added()     and self.deleted():
            if self.deleted_same_as_added():
                return 'EDT'
            else:
                return 'RES'
        if self.added()     and not self.deleted():
            return 'ADD'
        if not self.added() and self.deleted():
            return 'DEL'

        return None

    def __str__(self):
        if self.event is not None:
            event = str(self.event)
        else:
            event = self.subject.name

        t = self._type()
        if t == 'EDT':
            return f"{event}: edited: room = {self.room}"
        if t == 'RES':
            return f"{event}: rescheduled: {self.deleted_start}--{self.deleted_end} -> {self.added_start}--{self.added_end}"
        if t == 'ADD':
            return f"{event}: added: {self.added_start}--{self.added_end}"
        if t == 'DEL':
            return f"{event}: deleted: {self.deleted_start}--{self.deleted_end}"
