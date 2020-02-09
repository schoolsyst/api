from rest_framework.serializers import *
from rest_framework.permissions import *
from .models import *
from common.utils import hyperlinked_field_method
from datetime import datetime

class ReportSerializer(ModelSerializer):
  class Meta:
    model = Report
    exclude = ('github_issue', 'published')

  def create(self, validated_data):
    validated_data['user'] = self.context['request'].user
    r = Report.objects.create(**validated_data)
    published, issue_number_or_res = r.publish_github_issue()

    if published:
      r.github_issue = issue_number_or_res
      r.published = datetime.now().isoformat()
      r.save()
    elif issue_number_or_res == 'quota_reached':
      print("Can't created github issue: Reached quota!!!1")
    else:
      from json import dumps
      print(f'Got {issue_number_or_res.status_code} response from gh api:')
      print(issue_number_or_res.json())
      print('----')

    return r

class ReportReadSerializer(ModelSerializer):
  user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())

  class Meta:
    model = Report
    fields = (
      'type',
      'language',
      'github_issue',
      'added',
      'happened',
      'published', 
      'title', 
      'content', 
      'url', 
      'browser', 
      'os', 
      'device', 
      'screen_size', 
      'resolved',
      'user',
      'uuid',
    )
