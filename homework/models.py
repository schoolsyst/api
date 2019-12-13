from django.db.models import *
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from learn.models import zero_to_one_validator, Note
import bleach

class Grade(Model):
    # Relations & IDs
    subject = ForeignKey(to='common.Subject',
                         related_name='grades',
                         on_delete=CASCADE)
    uuid = UUIDField("UUID",
                     default=uuid.uuid4,
                     editable=False,
                     unique=True)
    #homeworks (M2M relationship stored in Homework)


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
    obtained = DateTimeField(blank=True, null=True)

    
    def __str__(self):
        return f"{self.subject.name}: {self.name}"


class Homework(Model):
    HW_TYPES = [
        ('TEST', 'Contrôle'),
        ('COURSEWORK', 'Devoir maison'),
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
    grades = ManyToManyField(Grade)

    name = CharField(max_length=300)
    type = CharField('Type', max_length=max(len(s) for s in HW_TYPES), choices=HW_TYPES)
    room = CharField(max_length=300, blank=True, null=True)
    progress = FloatField(validators=zero_to_one_validator, default=0)
    # Dates
    due = DateTimeField(blank=True, null=True)
    added = DateTimeField(blank=True, null=True)
    completed = DateTimeField(blank=True, null=True)
    # Fields containing user-controllable raw HTML (to be cleaned)
    details = TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Sanitize user-controllable HTML text
        self.details = bleach.clean(self.details)

        return super(Homework, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject.name}: {self.name}"
