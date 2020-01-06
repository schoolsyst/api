from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import register, ModelAdmin, SimpleListFilter
from common.models import *
from common.utils import auto_list_display


@register(Subject)
class SubjectAdmin(ModelAdmin):
	list_display = ('uuid', 'user', 'name', 'color', 'slug', 'room', 'weight', 'goal')
	list_editable = ('name', 'color', 'goal', 'weight', 'room')


@register(Setting)
class SettingAdmin(ModelAdmin):
	list_display = ('uuid', 'user', 'setting', 'value')
	list_editable = ('setting','value')
	list_filter = ('user', 'setting')


@register(SettingDefinition)
class SettingDefinitionAdmin(ModelAdmin):
	list_display = ('uuid','key', 'type', 'multiple', 'positive', 'optional', 'category', 'name', 'default')
	list_editable = ('key','type', 'multiple', 'positive', 'optional', 'category', 'name', 'default')

@register(User)
class UserAdmin(ModelAdmin):
	list_display = ('ip_address', 'username', 'is_superuser', 'email',
		'date_joined', 'setup_step', 'using_schedule')
	list_editable = ('username', 'email',)
	list_filter = ('is_superuser', 'date_joined')
