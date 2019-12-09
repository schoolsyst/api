from django.db.models import *
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

zero_to_one_validator = [
    MinValueValidator(0, "This can't be a negative value"),
    MaxValueValidator(1, "This should be a value between 0 and 1")
]


class Note(Model):
    FORMATS = [
        ('MARKDOWN', 'Markdown'),
        ('ASCIIDOC', 'AsciiDoc'),
        ('STUDENTML', 'StudentML'),
        ('HTML', 'HTML'),
    ]

    # Relations & IDs
    subject = ForeignKey(to='common.Subject',
                         related_name='notes',
                         on_delete=CASCADE)
    uuid = UUIDField("UUID",
                     default=uuid.uuid4,
                     editable=False,
                     unique=True)
    #homeworks (M2M relationship stored in Homework)
    #learndatas (M2M relationship stored in Learndata)

    name = CharField(max_length=300, blank=True, null=True)
    content = TextField(blank=True, null=True)
    format = CharField(max_length=50,
                       default=FORMATS[0],
                       choices=FORMATS)
    # Dates
    modified = DateTimeField(blank=True, null=True)
    opened = DateTimeField(auto_now=True)
    added = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or 'Untitled'


class Learndata(Model):
    # Relations & IDs
    subject = ForeignKey(to='common.Subject',
                         related_name='learndatas',
                         on_delete=CASCADE)
    uuid = UUIDField("UUID", default=uuid.uuid4, editable=False, unique=True)
    notes = ManyToManyField(Note)

    # Essentials
    data = TextField('JSON/YAML Content', blank=True, null=True)
    name = CharField(max_length=300, blank=True, null=True)
    progress = FloatField('Learning progress',
                          validators=zero_to_one_validator,
                          default=0)
    # Metadata: stats
    test_tries = IntegerField('Tries in testing mode',
                              validators=[MinValueValidator(0)],
                              default=0)
    train_tries = IntegerField('Tries in training mode',
                               validators=[MinValueValidator(0)],
                               default=0)
    time_spent = DurationField('Time spent on learning')

    # Metadata: dates
    opened = DateTimeField(auto_now=True)
    added = DateTimeField(auto_now=True)
    modified = DateTimeField(auto_now=True)
