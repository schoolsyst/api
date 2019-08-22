from django.utils.translation import gettext as _
from django.db.models import *

WEEK_DAYS = [
    ('monday',   _("Monday")),
    ('tuesday',  _("Tuesday")),
    ('wednesday',_("Wednesday")),
    ('thursday', _("Thursday")),
    ('friday',   _("Friday")),
    ('saturday', _("Saturday")),
    ('sunday',   _("Sunday"))
]

WEEK_TYPES = [
    ('both', 'Both'),
    ('Q1', 'Q1'),
    ('Q2', 'Q2'),
]

# Create your models here.
class Event(Model):
    subject  = ForeignKey(to='common.Subject',
                          related_name='events',
                          on_delete=CASCADE)

    start     = TimeField()
    end       = TimeField()
    room      = CharField(max_length=100)
    day       = CharField(choices=WEEK_DAYS, max_length=max([len(e[0]) for e in WEEK_DAYS]))
    week_type = CharField(choices=WEEK_TYPES,max_length=max([len(e[0]) for e in WEEK_TYPES]), default=WEEK_TYPES[0])
    
    def __str__(self):
        return f"{self.subject} at {self.day} ({self.week_type}) -- {self.start} to {self.end}"
    

class Deletion(Model):
    event   = OneToOneField(to='schedule.Event',
                            related_name='deletion',
                            on_delete=CASCADE)
    
    date    = DateField()
    
    def __str__(self):
        return self.event.__str__()
    
    
class Addition(Model):
    subject = ForeignKey(to='common.Subject',
                         related_name='schedule_additions',
                         on_delete=CASCADE)

    start   = TimeField()
    end     = TimeField()
    room    = CharField(max_length=100)
    date    = DateField()
    
    def __str__(self):
        return f"{self.subject} at {self.date} -- {self.start} to {self.end}"
    
    
class Exercise(Model):
    event   = ForeignKey(to='schedule.Event',
                         related_name='exercises',
                         on_delete=CASCADE)
    
    name    = CharField(max_length=400)
    due     = DateField()
    room    = CharField(max_length=100)
    created = DateTimeField(auto_now_add=True)
    notes   = TextField(blank=True, null=True)
    completed = BooleanField(default=False)
    
    def __str__(self):
        return self.name
