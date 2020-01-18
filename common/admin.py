from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import register, ModelAdmin, SimpleListFilter
from common.models import *
from common.utils import auto_list_display


@register(Subject)
class SubjectAdmin(ModelAdmin):
	list_display = ('uuid', 'user', 'name', 'color', 'slug', 'room', 'weight', 'goal')
	list_editable = ('name', 'color', 'goal', 'weight', 'room')

@register(User)
class UserAdmin(ModelAdmin):
	list_display = ('ip_address', 'username', 'is_superuser', 'email',
		'date_joined', 'setup_step', 'remaining_daily_github_issues')
	list_editable = ('username', 'email',)
	list_filter = ('is_superuser', 'date_joined')

@register(UserSettings)
class UserSettingsAdmin(ModelAdmin):
	list_display = ('user',)
