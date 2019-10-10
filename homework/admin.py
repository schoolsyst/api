from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import register, ModelAdmin
from .models import *
from common.utils import auto_list_display

@register(Grade)
class GradeAdmin(ModelAdmin):
    list_display = auto_list_display(Grade)

@register(Homework)
class HomeworkAdmin(ModelAdmin):
    list_display = auto_list_display(Homework)