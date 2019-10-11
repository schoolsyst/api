from django.db.models import *
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from learn.models import zero_to_one_validator


# Create your models here.
class Homework(Model):
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
    # Dates
    due = DateTimeField(blank=True, null=True)
    created = DateTimeField(blank=True, null=True)
    completed = DateTimeField(blank=True, null=True)
    room = CharField(max_length=300, blank=True, null=True)
    progress = FloatField(validators=zero_to_one_validator, default=0)
    is_test = BooleanField()


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
                      validators=[MinValueValidator(0)],
                      default=20)
    weight = FloatField('Grade weight',
                        validators=[MinValueValidator(0)],
                        default=1)
    
    # Added
    added = DateTimeField()
