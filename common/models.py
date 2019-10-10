from backend.settings import AUTH_USER_MODEL
import uuid
from django.db.models import *
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator
from learn.models import zero_to_one_validator

hex_color_validator = [RegexValidator(r'#(?:[A-Fa-f0-9]{3}){1,2}',
                                      "Please use a valid hexadecimal color format, eg. #268CCE, or #FFF")]
abbreviation_validator = [RegexValidator(r'[a-z_\-]{2,3}',
                                         "Please use exactly 2 or 3 lower-case letters (- and _ are also accepted)")]


class User(AbstractUser):
    ip_address = GenericIPAddressField(verbose_name="IP Address",
                                       blank=True,
                                       null=True)
    logged_in = DateTimeField(verbose_name="Last login date", auto_now=True)


class Setting(Model):
    # Relations & IDs
    setting = ForeignKey(to='common.DefaultSetting', on_delete=CASCADE)
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


class DefaultSetting(Model):
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
    color = CharField(max_length=7, validators=hex_color_validator)
    name = CharField(max_length=300)
    slug = SlugField(max_length=300)
    abbreviation = CharField(max_length=3, validators=abbreviation_validator)
    # Grades
    goal = FloatField(validators=zero_to_one_validator, null=True, blank=True)
    weight = FloatField(validators=[MinValueValidator(0, "The grade's weight cannot be negative")],
                        default=1)
    # Defaults
    room = CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s {self.name}"
