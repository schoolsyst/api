from django.db.models import *
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator, ValidationError
from common.utils import all_h_tags
import bleach
import re

zero_to_one_validator = [
    MinValueValidator(0, "This can't be a negative value"),
    MaxValueValidator(1, "This can't be greater than 1")
]



ALLOWED_HTML_TAGS = [
    *bleach.sanitizer.ALLOWED_TAGS,
    *['p', 'dl', 'dd', 'dt', 'img', 
      'svg', 'span', 'div', 's', 'hr',
      'sub', 'sup', 'code', 'table', 
      'tr', 'td', 'th', 'tbody', 'thead',
      'pre', 'br', 'u'],
    *all_h_tags()
]

ALLOWED_HTML_ATTRS = {
    **bleach.sanitizer.ALLOWED_ATTRIBUTES,
    **{
        'img': ['src', 'alt'],
        'svg': ['src', 'alt'],
        'span': ['style', 'class'],
        'div': ['style', 'class']
    },
    **all_h_tags(['id'])
}

ALLOWED_HTML_STYLES = {
    'color', 'background-color'
}

class Note(Model):
    FORMATS = [
        ('MARKDOWN', 'Markdown'),
        ('ASCIIDOC', 'AsciiDoc'),
        ('STUDENTML', 'StudentML'),
        ('HTML', 'HTML'),
        ('LINK', 'Application externe')
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
    format = CharField(max_length=50,
                       default=FORMATS[0],
                       choices=FORMATS)
    # Dates
    modified = DateTimeField(blank=True, null=True)
    opened = DateTimeField(auto_now=True)
    added = DateTimeField(auto_now=True)

    # Fields containing user-controllable, raw HTML
    content = TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # For external notes, verify that the content contains an url, and strip spaces
        if self.format == 'LINK':
            try:
                URLValidator(self.content)
            except ValidationError:
                raise ValidationError
        # For HTML notes, sanitize user-controllable HTML text
        elif self.format == 'HTML':
            self.content = bleach.clean(
                self.content,
                tags=ALLOWED_HTML_TAGS,
                attributes=ALLOWED_HTML_ATTRS,
                styles={
                    'span': ALLOWED_HTML_STYLES,
                    'class': ALLOWED_HTML_STYLES
                }
            )


        return super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject}: {self.name or '<Untitled>'}"


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
