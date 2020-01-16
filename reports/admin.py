from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.contrib.admin import register, ModelAdmin, SimpleListFilter
from .models import *
from common.utils import auto_list_display

# Register your models here.
@register(Report)
class ReportAdmin(ModelAdmin):
  list_display = ('uuid', 'type', 'user', 'title', 'github_issue_link')

  def github_issue_link(self, obj):
    if not obj.github_issue: return None
    return format_html(
      '<a target="_blank"'
      'href="https://github.com/schoolsyst/frontend/issues/{issue}">'
      '#{issue}</a>',
      issue=obj.github_issue
    )
  github_issue_link.short_description = "Github issue"
