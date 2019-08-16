from rest_framework.serializers import *
from common.models import Subject
from common.serializers import *
from .models import *

class EventSerializer(ModelSerializer):
    subject = SlugRelatedField(slug_field='slug', queryset=Subject.objects.all())
    class Meta:
        model = Event
        fields = '__all__'

class EventReadSerialier(ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'
        
class AdditionSerializer(ModelSerializer):
    subject = SlugRelatedField(slug_field='slug', queryset=Subject.objects.all())
    class Meta:
        model = Addition
        fields = '__all__'

class AdditionReadSerialier(ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    class Meta:
        model = Addition
        fields = '__all__'

class DeletionSerializer(ModelSerializer):
    event = PrimaryKeyRelatedField(queryset=Event.objects.all())
    class Meta:
        model = Deletion
        fields = '__all__'

class DeletionReadSerialier(ModelSerializer):
    event = EventSerializer(read_only=True)
    class Meta:
        model = Deletion
        fields = '__all__'

class ExerciseSerializer(ModelSerializer):
    event = PrimaryKeyRelatedField(queryset=Event.objects.all())
    class Meta:
        model = Exercise
        fields = '__all__'

class ExerciseReadSerialier(ModelSerializer):
    event = EventSerializer(read_only=True)
    class Meta:
        model = Exercise
        fields = '__all__'
