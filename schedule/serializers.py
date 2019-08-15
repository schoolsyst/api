from rest_framework.serializers import *
from common.models import Subject
from common.serializers import *
from .models import *

class EventSerializer(ModelSerializer):
    subject = SubjectSerializer()
    class Meta:
        model = Event
        
        fields = '__all__'
        

class AdditionSerializer(ModelSerializer):
    subject = SubjectSerializer()
    class Meta:
        model = Addition
        
        fields = '__all__'

class DeletionSerializer(ModelSerializer):
    subject = SubjectSerializer()
    class Meta:
        model = Deletion
        
        fields = '__all__'

class ExerciseSerializer(ModelSerializer):
    event = EventSerializer()
    class Meta:
        model = Exercise
        
        fields = '__all__'









