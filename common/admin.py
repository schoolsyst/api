from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import register, ModelAdmin
from common.models import *
from common.utils import auto_list_display


@register(Subject)
class SubjectAdmin(ModelAdmin):
    list_display = ('uuid', 'user', 'name', 'abbreviation',
                    'color', 'slug', 'room', 'weight', 'goal')
    list_editable = ('name', 'abbreviation', 'color', 'slug', 'goal')


@register(Setting)
class SettingAdmin(ModelAdmin):
    list_display = ('uuid', 'user', 'setting', 'value')
    list_editable = ('setting',)


@register(SettingDefinition)
class SettingDefinitionAdmin(ModelAdmin):
    list_display = ('key', 'type', 'multiple', 'positive', 'optional', 'category', 'name', 'default')
    list_editable = ('type', 'multiple', 'positive', 'optional', 'category', 'name')


@register(User)
class UserAdmin(ModelAdmin):
    list_display = ('ip_address', 'username', 'is_superuser', 'email',
                    'date_joined')
    list_editable = ('username', 'email',)
