from django.contrib.admin import register, ModelAdmin
from .models import *
from common.utils import auto_list_display

@register(Event)
class EventAdmin(ModelAdmin):
    list_display = ('uuid', 'subject', 'week_type', 'day', 'start', 'end', 'room')
    list_editable = ('subject', 'week_type', 'day', 'start', 'end', 'room')

@register(Mutation)
class MutationAdmin(ModelAdmin):
    list_display = ('uuid', 'type', 'event', 'deleted_start', 'deleted_end', 'added_start', 'added_end', 'room')
    list_editable = ('deleted_start', 'deleted_end', 'added_start', 'added_end', 'room')
