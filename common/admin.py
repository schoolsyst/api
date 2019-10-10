from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import register, ModelAdmin
from common.models import *
from common.utils import auto_list_display

@register(Subject)
class SubjectAdmin(ModelAdmin):
    list_display = ('uuid', 'user', 'name', 'abbreviation', 'color', 'slug', 'room', 'weight', 'goal')

@register(Setting)
class SettingAdmin(ModelAdmin):
    list_display = auto_list_display(Setting)

@register(DefaultSetting)
class DefaultSettingAdmin(ModelAdmin):
    list_display = ('key', 'type', 'category', 'name', 'default')

@register(User)
class UserAdmin(ModelAdmin):
    list_display = ('username', 'is_superuser', 'email', 'ip_address', 'date_joined')