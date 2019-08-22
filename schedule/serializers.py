from rest_framework.serializers import *
from common.models import Subject
from common.serializers import *
from .models import *

class EventSerializer(ModelSerializer):
    subject = SlugRelatedField(slug_field='slug', queryset=Subject.objects.all())
    class Meta:
        model = Event
        fields = '__all__'

class EventReadSerializer(ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'
        
class AdditionSerializer(ModelSerializer):
    subject = SlugRelatedField(slug_field='slug', queryset=Subject.objects.all())
    class Meta:
        model = Addition
        fields = '__all__'

class AdditionReadSerializer(ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    class Meta:
        model = Addition
        fields = '__all__'

class DeletionSerializer(ModelSerializer):
    event = PrimaryKeyRelatedField(queryset=Event.objects.all())
    class Meta:
        model = Deletion
        fields = '__all__'

class DeletionReadSerializer(ModelSerializer):
    event = EventSerializer(read_only=True)
    class Meta:
        model = Deletion
        fields = '__all__'

class ExerciseSerializer(ModelSerializer):
    subject = SlugRelatedField(queryset=Subject.objects.all(), slug_field="slug")
    class Meta:
        model = Exercise
        fields = '__all__'

class ExerciseReadSerializer(ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    class Meta:
        model = Exercise
        fields = '__all__'
