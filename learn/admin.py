from django.contrib.admin import register, ModelAdmin
from learn.models import Note, Learndata
from common.utils import auto_list_display


@register(Note)
class NoteAdmin(ModelAdmin):
    list_display = ('uuid', 'subject', 'name',
                    'modified', 'added', 'format')
    list_editable = ('name', 'format')


@register(Learndata)
class LearndataAdmin(ModelAdmin):
    list_display = ('uuid', 'subject', 'name', 'opened', 'added',
                    'progress', 'test_tries', 'train_tries', 'time_spent')
    list_editable = ('name', 'progress')
