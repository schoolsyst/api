from backend.settings import AUTH_USER_MODEL
import uuid
from django.db.models import *
from django.core.validators import RegexValidator

# Create your models here.
class Report(Model):
    from datetime import timedelta
    REPORT_TYPES = [
      ('BUG', 'Bug'),
      ('FEATURE', 'Fonctionnalité')
    ]
    LANGUAGES = [
      ('fr', 'Français'),
      ('en', 'English')
    ]
    DEVICES = [
      ('PHONE', 'Smartphone'),
      ('TABLET', 'Tablette'),
      ('LAPTOP', 'Ordinateur portable'),
      ('DESKTOP', 'Ordinateur fixe'),
      ('SMARTWATCH', 'Montre connectée'),
      ('OTHER', 'Autre'),
    ]

    # Relations & IDs
    user = ForeignKey(to=AUTH_USER_MODEL,
                      on_delete=CASCADE,
                      related_name='reports')
    uuid = UUIDField("UUID",
                     default=uuid.uuid4,
                     editable=False,
                     unique=True)
    # Metadata
    type = CharField(max_length=max([ len(o[0]) for o in REPORT_TYPES ]), choices=REPORT_TYPES)
    language = CharField(max_length=max([ len(o[0]) for o in LANGUAGES ]), choices=LANGUAGES)
    github_issue = PositiveIntegerField(blank=True, null=True)
    # Dates
    added = DateTimeField(auto_now=True)
    happened = DateTimeField(blank=True, null=True)
    published = DateTimeField(blank=True, null=True)
    # Message
    title = CharField(max_length=30, blank=True, null=True)
    content = TextField()
    # Troubleshooting metadata
    url = URLField(default="Unknown")
    browser = CharField(default="Unknown", max_length=200)
    os = CharField(default="Unknown", max_length=200)
    device = CharField(default="Unknown", max_length=max([ len(o[0]) for o in DEVICES ]), choices=DEVICES)
    screen_size = CharField(default="Unknown", max_length=200, validators=[RegexValidator(r'(?:Unknown)|(?:(\d+)x(\d+))')])

    def __str__(self):
        return f"{self.user.username}'s {self.title or self.content[0:30]}"

    @property
    def on_github(self) -> bool:
      return self.github_issue is not None

    def as_github_issue(self):
      import pypandoc
      is_bug = self.type == 'BUG'
      front_matter = f"""
| Reported by          | URL        | OS        | Browser        | Device type   |{ " Bug happened at |" if is_bug else ''}
|----------------------|------------|-----------|----------------|---------------|{ "-----------------|" if is_bug else ''}
| {self.user.username} | {self.url} | {self.os} | {self.browser} | {self.device} |{ f" {self.happened} |" if is_bug else ''}
"""
      return {
        'title': self.title or self.content[0:30],
        'body': front_matter.strip() + '\n\n' + self.content,
        'assignees': ['ewen-lbh'],
        'labels': [
          'lang:' + self.language,
          {'FEATURE': 'enhancement', 'BUG': 'bug'}[self.type],
          'from:schoolsyst.com'
        ]
      }

    def publish_github_issue(self):
      if self.user.remaining_daily_github_issues <= 0: return False, 'quota_reached'
      import requests, json
      from os import environ
      # key = environ.get('GITHUB_API_KEY')
      key = '26637329000bc14d8dc0afd591414077b8b6154e' #XXX
      if key is None: raise Exception('Please set the environment variable GITHUB_API_KEY')
      print(f'GITHUB_API_KEY={key}')

      data = self.as_github_issue()

      print(json.dumps(data))

      repo = 'ewen-lbh/gh-api-playground' if DEBUG else 'schoolsyst/frontend'
      res = requests.post(
        f'https://api.github.com/repos/{repo}/issues',
        json=data,
        auth=('ewen-lbh', key)
      )

      if str(res.status_code).startswith('2'):
        return (True, res.json()['number'])
      return (False, res)

      return False, None


