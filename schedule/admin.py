from django.contrib.admin import register, ModelAdmin
from .models import *
from common.utils import auto_list_display

@register(Addition)
class AdditionAdmin(ModelAdmin):
    list_display = auto_list_display(Addition)

@register(Deletion)
class DeletionAdmin(ModelAdmin):
    list_display = auto_list_display(Deletion)

@register(Event)
class EventAdmin(ModelAdmin):
    list_display = auto_list_display(Event)

@register(Exercise)
class ExerciseAdmin(ModelAdmin):
    list_display = auto_list_display(Exercise)