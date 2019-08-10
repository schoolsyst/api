from rest_framework.serializers import *
from .models import *

class NotionSerializer(ModelSerializer):
    class Meta:
        model = Notion
        
        fields = '__all__'
        depth = 4
 
class TestSerializer(ModelSerializer):
    class Meta:
        model = Test
        
        fields = '__all__'
        depth = 4

class GradeSerializer(ModelSerializer):
    class Meta:
        model = Grade
        
        fields = '__all__'
        depth = 4

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        
        fields = '__all__'
        depth = 4

