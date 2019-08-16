from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'is_superuser', 'email', 'ip_address', 'date_joined')

admin.site.register(User, CustomUserAdmin)