from backend.settings import AUTH_USER_MODEL
import uuid
from django.db.models import *
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator, MinValueValidator
from learn.models import zero_to_one_validator

HEX_COLOR_VALIDATOR = [RegexValidator(r'#(?:[A-Fa-f0-9]{3}){1,2}',
                                      "Please use a valid hexadecimal color format, eg. #268CCE, or #FFF")]
ABBREVIATION_VALIDATOR = [RegexValidator(r'[^\s]{,3}',
                                         "Please use at most 3 non-space characters")]


class UsernameValidator(UnicodeUsernameValidator):
    regex = r'^.+$'

# TODO: case-insensitive checks


class User(AbstractUser):
    username_validator = UsernameValidator()

    ip_address = GenericIPAddressField(verbose_name="IP Address",
                                       blank=True,
                                       null=True)


class Setting(Model):
    # Relations & IDs
    setting = ForeignKey(to='common.SettingDefinition', on_delete=CASCADE)
    user = ForeignKey(to=AUTH_USER_MODEL,
                      on_delete=CASCADE,
                      related_name='settings')
    uuid = UUIDField("UUID",
                     default=uuid.uuid4,
                     editable=False,
                     unique=True)

    value = TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s {self.setting.name}"


class SettingDefinition(Model):
    TYPES = [
        ('TEXT',      'Texte'),
        ('DATETIME',  'Date & heure'),
        ('DATE',      'Date'),
        ('DATERANGE', 'Plage de date'),
        ('TIME',      'Heure'),
        ('TIMERANGE', 'Plage horaire'),
        ('SELECT',    'Choix'),
        ('INTEGER',   'Nombre entier'),
        ('FLOAT',     'Nombre décimal'),
        ('BOOLEAN',   'Booléen (oui/non)')
    ]
    max_kind_len = max([len(k[0]) for k in TYPES])

    uuid = UUIDField("UUID",
                     default=uuid.uuid4,
                     editable=False,
                     unique=True)
    # Naming
    key = CharField(max_length=300, unique=True)
    name = CharField(max_length=200)
    category = CharField(max_length=150)
    description = TextField(blank=True, null=True)
    # Value definition
    type = CharField(choices=TYPES,
                     max_length=max_kind_len,
                     default=TYPES[0])
    optional = BooleanField(default=True)
    choices = TextField(blank=True, null=True)  # Comma-separated
    default = TextField(blank=True, null=True)
    positive = BooleanField(default=False)
    multiple = BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class Subject(Model):
    # Relations & IDs
    user = ForeignKey(to=AUTH_USER_MODEL,
                      on_delete=CASCADE,
                      related_name='subjects')
    uuid = UUIDField("UUID",
                     default=uuid.uuid4,
                     editable=False,
                     unique=True)
    # Naming
    color = CharField(max_length=7, validators=HEX_COLOR_VALIDATOR)
    name = CharField(max_length=300)
    slug = SlugField(max_length=300)
    abbreviation = CharField(max_length=3, validators=ABBREVIATION_VALIDATOR)
    # Grades
    goal = FloatField(validators=zero_to_one_validator, null=True, blank=True)
    weight = FloatField(validators=[MinValueValidator(0, "The grade's weight cannot be negative")],
                        default=1)
    # Defaults
    room = CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return '{1} ({0})'.format(self.user.username, self.name)
