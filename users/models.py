from django.contrib.auth.models import AbstractUser
from django.db.models import *

class User(AbstractUser):
    ip_address = GenericIPAddressField(verbose_name="IP Address", blank=True, null=True)
    joined = DateField(auto_now=True)