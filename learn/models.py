from django.db.models import *
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

zero_to_one_validator = [
    MinValueValidator(0, "This can't be a negative value"),
    MaxValueValidator(1, "This should be a value between 0 and 1")
]


class Note(Model):
    FILETYPES = [
        ('MARKDOWN', 'Markdown'),
        ('ASCIIDOC', 'AsciiDoc'),
        ('STUDENTML', 'StudentML'),
    ]

    # Relations & IDs
    subject = ForeignKey(to='common.Subject',
                         related_name='notes',
                         on_delete=CASCADE)
    uuid = UUIDField("UUID",
                     default=uuid.uuid4,
                     editable=False,
                     unique=True)

    name = CharField(max_length=300)
    content = TextField(blank=True, null=True)
    created = DateTimeField()
    filetype = CharField(max_length=50,
                         default=FILETYPES[0],
                         choices=FILETYPES)
    last_modified = DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Learndata(Model):
    # Relations & IDs
    subject = ForeignKey(to='common.Subject',
                         related_name='learndatas',
                         on_delete=CASCADE)
    note = ForeignKey(to='learn.Note',
                      related_name='learndatas',
                      on_delete=SET_NULL,
                      blank=True,
                      null=True)
    uuid = UUIDField("UUID", default=uuid.uuid4, editable=False, unique=True)
    # Essentials
    data = TextField('YAML Content', blank=True, null=True)
    name = CharField(max_length=300)
    learnt = FloatField('Learning progress',
                        validators=zero_to_one_validator,
                        default=0)
    # Metadata: stats
    test_tries = IntegerField('Tries in testing mode',
                              validators=[MinValueValidator(0)],
                              default=0)
    train_tries = IntegerField('Tries in training mode',
                               validators=[MinValueValidator(0)],
                               default=0)
    # Metadata: dates & durations
    last_opened = DateTimeField(auto_now=True)
    time_spent = DurationField('Time spent on learning')
