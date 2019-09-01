from backend.settings import AUTH_USER_MODEL
import uuid
from django.db.models import *
from django.core.validators import RegexValidator, MinValueValidator
from learn.models import zero_to_one_validator

hex_color_validator    = [RegexValidator(r'#(?:[A-Fa-f0-9]{3}){1,2}', 
                                         "Please use a valid hexadecimal color format, eg. #268CCE, or #FFF")]
abbreviation_validator = [RegexValidator(r'[a-z_\-]{3}',
                                         "Please use exactly 3 lower-case letters (- and _ are also accepted)")]

class Setting(Model):
    setting  = ForeignKey(to='common.DefaultSetting', on_delete=CASCADE)
    user     = ForeignKey(to=AUTH_USER_MODEL,
                          on_delete=CASCADE,
                          related_name='settings')
    uuid     = UUIDField("UUID", 
                         default=uuid.uuid4, 
                         editable=False, 
                         unique=True)

    value    = TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s {self.setting.name}"

class DefaultSetting(Model):
    KINDS = [
        ('datetime', 'Date & heure'),
        ('date', 'Date'),
        ('dates', 'Dates'),
        ('daterange', 'Plage de dates'),
        ('dateranges', 'Plages de dates'),
        ('time', 'Heure'),
        ('times', 'Heures'),
        ('timerange', 'Plage horaire'),
        ('timeranges', 'Plages horaires'),
        ('choices', 'Choix'),
        ('text', 'Texte'),
        ('posint', 'Nombre entier positif'),
        ('int', 'Nombre entier'),
        ('float', 'Nombre décimal'),
        ('posfloat', 'Nombre décimal positif'),
        ('boolean', 'Booléen (oui/non)')
    ]
    max_kind_len = max([len(k) for k in KINDS[0]])

    key         = CharField(max_length=100, unique=True)
    name        = CharField(max_length=200)
    namespace   = CharField(max_length=150)
    kind        = CharField(choices=KINDS, max_length=max_kind_len, default="text")
    required    = BooleanField(default=False)
    description = TextField(blank=True, null=True)
    choices     = TextField(blank=True, null=True) # Comma-separated
    default     = TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class Subject(Model):
    user     = ForeignKey(to=AUTH_USER_MODEL,
                          on_delete=CASCADE,
                          related_name='subjects')
    uuid     = UUIDField("UUID", 
                         default=uuid.uuid4, 
                         editable=False, 
                         unique=True)
    # Naming
    color        = CharField(max_length=7, validators=hex_color_validator)
    name         = CharField(max_length=100)
    slug         = SlugField(max_length=100)
    abbreviation = CharField(max_length=3, validators=abbreviation_validator)
    room         = CharField(max_length=100, blank=True, null=True)
    grade_goal   = FloatField(validators=zero_to_one_validator, null=True, blank=True)
    physical_weight = FloatField(validators=[MinValueValidator(0, "This can't be a negative value")], default=0)
    
    def __str__(self):
        return f"{self.user.username}'s {self.name}"