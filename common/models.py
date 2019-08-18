from backend.settings import AUTH_USER_MODEL
from django.db.models import *
from django.core.validators import RegexValidator, MinValueValidator
from learn.models import zero_to_one_validator

hex_color_validator    = [RegexValidator(r'#(?:[A-Fa-f0-9]{3}){1,2}', 
                                         "Please use a valid hexadecimal color format, eg. #268CCE, or #FFF")]
abbreviation_validator = [RegexValidator(r'[a-z_\-]{3}',
                                         "Please use exactly 3 lower-case letters (- and _ are also accepted)")]
class Setting(Model):
    user     = ForeignKey(to=AUTH_USER_MODEL,
                          on_delete=CASCADE,
                          related_name='settings')
    
    name     = CharField(max_length=50, unique=True)
    value    = TextField()
    
    def __str__(self):
        return self.name
    
class Subject(Model):
    user     = ForeignKey(to=AUTH_USER_MODEL,
                          on_delete=CASCADE,
                          related_name='subjects')
    # Naming
    color        = CharField(max_length=7, validators=hex_color_validator)
    name         = CharField(max_length=100)
    slug         = SlugField(max_length=100)
    abbreviation = CharField(max_length=3, validators=abbreviation_validator)
    room         = CharField(max_length=50, null=True, blank=True)
    grade_goal   = FloatField(validators=zero_to_one_validator, null=True, blank=True)
    physical_weight = FloatField(validators=[MinValueValidator(0, "This can't be a negative value")], default=0)
    
    def __str__(self):
        return self.name