from rest_framework.serializers import *
from common.models import Subject
from common.serializers import *
from .models import *


class EventSerializer(ModelSerializer):
    subject = SlugRelatedField(
        slug_field='slug', queryset=Subject.objects.all())

    class Meta:
        model = Event
        fields = '__all__'


class EventReadSerializer(ModelSerializer):
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


class EventSerializer(ModelSerializer):
    event = SlugRelatedField(slug_field='uuid', queryset=Event.objects.all())

    class Meta:
        model = Event
        fields = '__all__'


class EventReadSerializer(ModelSerializer):
    event = EventReadSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
