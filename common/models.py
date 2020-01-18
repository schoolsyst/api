from backend.settings import AUTH_USER_MODEL
import uuid
from django.db.models import *
from django_extensions.db.fields import AutoSlugField
from slugify import slugify
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator, MinValueValidator
from learn.models import zero_to_one_validator
from datetime import datetime, date
current_year = datetime.now().year

HEX_COLOR_VALIDATOR = [RegexValidator(r'^#(?:[A-Fa-f0-9]{3}){1,2}$',
                                      "Please use a valid hexadecimal color format, eg. #268CCE, or #FFF")]
ABBREVIATION_VALIDATOR = [RegexValidator(r'^[^\s]{,3}$',
                                         "Please use at most 3 non-space characters")]


class UsernameValidator(UnicodeUsernameValidator):
    regex = r'^.+$'

# TODO: case-insensitive checks

class UserSettings(Model):
    def __str__(self):
        return f"{self.user}'s settings"
    
    THEMES = [
        ('LIGHT', 'Clair'),
        ('DARK', 'Sombre'),
        ('AUTO', 'Automatique')
    ]
    
    year_start = DateField("Rentrée", blank=True, null=True)
    trimester_2_start = DateField("Début du second trimestre", blank=True, null=True)
    trimester_3_start = DateField("Début du troisième trimestre", blank=True, null=True)
    year_end = DateField("Fin de l'année scolaire", blank=True, null=True)
    theme = CharField(max_length=50, default='AUTO', choices=THEMES)
    show_completed_exercises = BooleanField("Afficher les exercices complétés", default=False)
    grades_unit = FloatField("Unité des notes", validators=[MinValueValidator(1)])
    grades_default_weight = FloatField("Coefficient par défaut", validators=[MinValueValidator(0)], default=1)
    @property
    def offdays(self):
        return Offday.objects.filter(user__id=self.user.id)
    #offdays = OneToMany: UserSettings 1..* Offday
    use_schedule = BooleanField("Utiliser l'emploi du temps", default=True)
    
    
    @property
    def current_trimester(self):
        now = datetime.now().date()
        idx = None
        
        if now < self.year_start: idx = None
        elif now < self.trimester_2_start: idx = 1
        elif now < self.trimester_3_start: idx = 2
        elif now < self.year_end: idx = 3
        else: idx = None
        
        return (idx, self.trimester_ranges(idx))
        
    def trimester_ranges(self, idx):
        if not self.has_year_settings: return None
        return {
            1: (self.start, self.trimester_2),
            2: (self.trimester_2, self.trimester_3),
            3: (self.trimester_3, self.end),
        }
    
    @property
    def has_year_settings(self):
        return (
            self.year_start is not None
            and self.trimester_2_start is not None
            and self.trimester_3_start is not None
            and self.year_end is not None
        )
        
class Offday(Model):
    user_settings = ForeignKey(UserSettings, CASCADE, related_name='offdays')
    start = DateField("Début")
    end = DateField("Fin")
    
class User(AbstractUser):
    WEEK_TYPES = [ (c, c) for c in ['Q1', 'Q2'] ]
    
    username_validator = UsernameValidator()
    email = EmailField(unique=True)
    ip_address = GenericIPAddressField(verbose_name="IP Address", blank=True, null=True)
    settings = OneToOneField(UserSettings, on_delete=CASCADE, blank=True, null=True)
    # Computed 
    @property
    def remaining_daily_github_issues(self):
        GITHUB_PUBLISH_LIMIT = 10 if self.is_superuser else 5
        from datetime import datetime
        # Get the user's reports for today
        reports = self.reports.filter(published__date=datetime.now().date())
        # Compare the number of reports against the limit
        return GITHUB_PUBLISH_LIMIT - reports.count()
    @property
    def setup_step(self):
        """
        Gives the setup step the user needs to complete before being able to use the app.
        `None` means that the user is ready to use the app.
        """
        if self.is_staff:
            return None
        subjects = self.subjects.all()
        has_subjects = subjects.count() > 0
        has_events = False
        for s in subjects:
            has_events = s.events.all().count() > 0

        if not has_subjects: return 'subjects'
        if self.settings is None: return 'schedule/settings'
        if self.settings.using_schedule and self.missing_schedule_settings: return 'schedule/settings'
        if self.settings.using_schedule and not has_events: return 'schedule/events'
        return None
    @property
    def missing_schedule_settings(self):
        return (
            self.settings.has_year_settings is None
        )

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.settings is None:
            settings = UserSettings.objects.create(
                user=self,
                grades_unit=20
            )
            self.settings = settings
            self.save()
            print(f"Attached UserSettings #{settings.id} to User #{self.id}")

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
    name = CharField(max_length=300)
    slug = AutoSlugField(populate_from=["name"], slugify_function=slugify)
    color = CharField(max_length=7, validators=HEX_COLOR_VALIDATOR)
    # Grades
    weight = FloatField(validators=[MinValueValidator(0, "The grade's weight cannot be negative")],
                        default=1)
    goal = FloatField(validators=zero_to_one_validator, null=True, blank=True)
    # Defaults
    room = CharField(max_length=300, blank=True, null=True)

    # Calculate slug (sadly, AutoSlugField does not update with name)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return '{0}: {1}'.format(self.user.username, self.slug)
