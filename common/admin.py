from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import register, ModelAdmin
from common.models import *
from common.utils import auto_list_display

@register(Subject)
class SubjectAdmin(ModelAdmin):
    list_display = auto_list_display(Subject)

@register(Setting)
class SettingAdmin(ModelAdmin):
    list_display = auto_list_display(Setting)

@register(DefaultSetting)
class DefaultSettingAdmin(ModelAdmin):
    list_display = auto_list_display(DefaultSetting)