from django.contrib.admin import register, ModelAdmin
from learn.models import Test, Note, Grade, Notion
from common.utils import auto_list_display

@register(Test)
class TestAdmin(ModelAdmin):
    list_display = auto_list_display(Test)

@register(Note)
class NoteAdmin(ModelAdmin):
    list_display = auto_list_display(Note)

@register(Grade)
class GradeAdmin(ModelAdmin):
    list_display = auto_list_display(Grade)

@register(Notion)
class NotionAdmin(ModelAdmin):
    list_display = ['pk','subject','name','slug','progress']