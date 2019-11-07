from django.db.models import *
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from learn.models import zero_to_one_validator


# Create your models here.
class Homework(Model):
    HW_TYPES = [
        ('TEST', 'Contrôle'),
        ('DM', 'Devoir maison'),
        ('EXERCISE', 'Exercice'),
        ('TOBRING', 'À apporter'),
    ]
    
    # Relations & IDs
    subject = ForeignKey(to='common.Subject',
                         related_name='homework',
                         on_delete=CASCADE)
    uuid = UUIDField("UUID",
                     default=uuid.uuid4,
                     editable=False,
                     unique=True)

    name = CharField(max_length=300)
    notes = TextField(blank=True, null=True)
    type = CharField('Type', max_length=max(len(s) for s in HW_TYPES), choices=HW_TYPES)
    room = CharField(max_length=300, blank=True, null=True)
    progress = FloatField(validators=zero_to_one_validator, default=0)
    # Dates
    due = DateTimeField(blank=True, null=True)
    added = DateTimeField(blank=True, null=True)
    completed = DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject.name}: {self.name}"
    


class Grade(Model):
    # Relations & IDs
    subject = ForeignKey(to='common.Subject',
                         related_name='grades',
                         on_delete=CASCADE)
    homework = ForeignKey(to='homework.Homework',
                          related_name='homework',
                          on_delete=SET_NULL,
                          blank=True,
                          null=True)
    uuid = UUIDField("UUID",
                     default=uuid.uuid4,
                     editable=False,
                     unique=True)
    name = CharField(max_length=300)

    # Values
    obtained = FloatField('Obtained grade',
                          validators=zero_to_one_validator,
                          blank=True,
                          null=True)
    expected = FloatField('Expected grade',
                          validators=zero_to_one_validator,
                          blank=True,
                          null=True)
    goal = FloatField('Grade goal',
                      validators=zero_to_one_validator,
                      blank=True,
                      null=True)
    # Values' context
    unit = FloatField('Grade unit',
                      validators=[MinValueValidator(1)],
                      default=20)
    weight = FloatField('Grade weight',
                        validators=[MinValueValidator(0)],
                        default=1)
    
    # Dates
    added = DateTimeField(auto_now=True)
    date_obtained = DateTimeField(blank=True, null=True)

    
    def __str__(self):
        return f"{self.subject.name}: {self.name}"
