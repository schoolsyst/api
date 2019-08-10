from rest_framework.serializers import *
from common.models import Subject
from .models import *

class EventSerializer(ModelSerializer):
    subject = SlugRelatedField(slug_field='slug', queryset=Subject.objects.all())
    class Meta:
        model = Event
        
        fields = '__all__'
        depth = 4
        

class AdditionSerializer(ModelSerializer):
    subject = SlugRelatedField(slug_field='slug', queryset=Subject.objects.all())
    class Meta:
        model = Addition
        
        fields = '__all__'
        depth = 4

class DeletionSerializer(ModelSerializer):
    event = PrimaryKeyRelatedField(queryset=Event.objects.all())
    class Meta:
        model = Deletion
        
        fields = '__all__'
        depth = 4

class ExerciseSerializer(ModelSerializer):
    class Meta:
        model = Exercise
        
        fields = '__all__'
        depth = 4









