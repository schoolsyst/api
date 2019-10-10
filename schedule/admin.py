from django.contrib.admin import register, ModelAdmin
from .models import *
from common.utils import auto_list_display

@register(Mutation)
class MutationAdmin(ModelAdmin):
    list_display = auto_list_display(Mutation)

@register(Event)
class EventAdmin(ModelAdmin):
    list_display = auto_list_display(Event)