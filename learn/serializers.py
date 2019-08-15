from rest_framework.serializers import *
from .models import *
from common.serializers import *

class NotionSerializer(ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = Notion
        
        fields = '__all__'
 
class TestSerializer(ModelSerializer):
    notions = NotionSerializer(many=True)

    class Meta:
        model = Test
        
        fields = '__all__'

class GradeSerializer(ModelSerializer):
    test = TestSerializer()
    class Meta:
        model = Grade
        
        fields = '__all__'


class NoteSerializer(ModelSerializer):
    notion = NotionSerializer(many=True)
    class Meta:
        model = Note
        
        fields = '__all__'

