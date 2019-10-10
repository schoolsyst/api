from django.contrib.admin import register, ModelAdmin
from learn.models import Note, Learndata
from common.utils import auto_list_display

@register(Note)
class NoteAdmin(ModelAdmin):
    list_display = auto_list_display(Note)

@register(Learndata)
class LearndataAdmin(ModelAdmin):
    list_display = auto_list_display(Learndata)