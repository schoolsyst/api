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

    start = TimeField()
    end = TimeField()
    room = CharField(max_length=300)
    day = IntegerField(choices=WEEK_DAYS)
    week_type = CharField(choices=WEEK_TYPES,
                          max_length=max([len(e[0]) for e in WEEK_TYPES]),
                          default=WEEK_TYPES[0])

    def __str__(self):
        return f"{self.subject} at {WEEK_DAYS[self.day][1]} ({self.week_type}) -- {self.start} to {self.end}"


class Mutation(Model):
    """
    Represents schedule mutations (rescheduled events, deleted events, even new events)
    """
    event = ForeignKey(to='schedule.Event',
                       related_name='mutations',
                       on_delete=SET_NULL,
                       blank=True,
                       null=True)
    uuid = UUIDField("UUID",
                     default=uuid.uuid4,
                     editable=False,
                     unique=True)

    deleted = DateField(blank=True, null=True)
    # If not `is_rescheduled()`, all the following fields (at least `rescheduled`) should be NULL:
    rescheduled = DateField(blank=True, null=True)
    start = TimeField(blank=True, null=True)
    end = TimeField(blank=True, null=True)
    room = CharField(max_length=300,
                     blank=True,
                     null=True)

    def is_rescheduled(self):
        return not self.rescheduled is None

    def __str__(self):
        first_part = f"{self.event.subject.name} {self.deleted}@{self.event.start}-{self.event.end}"

        if self.is_rescheduled():
            other_part = f"-> {self.rescheduled}@{self.start}-{self.end}"
        else:
            other_part = "deleted"

        return f"{first_part} {other_part}"
