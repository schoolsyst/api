from django.contrib.admin import register, ModelAdmin
from learn.models import Test, Note, Grade
from common.utils import auto_list_display

@register(Test)
class TestAdmin(ModelAdmin):
    list_display = ['uuid', 'subject', 'due', 'details']

@register(Note)
class NoteAdmin(ModelAdmin):
    list_display = auto_list_display(Note)

@register(Grade)
class GradeAdmin(ModelAdmin):
    list_display = auto_list_display(Grade)