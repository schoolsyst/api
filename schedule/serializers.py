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
    subject_url = SerializerMethodField()
    get_subject_url = hyperlinked_field_method('subject')

    class Meta:
        model = Event
        fields = '__all__'


class MutationSerializer(ModelSerializer):
    event = SlugRelatedField(slug_field='uuid', queryset=Event.objects.all())

    class Meta:
        model = Mutation
        fields = '__all__'


class MutationReadSerializer(ModelSerializer):
    event = EventReadSerializer(read_only=True)
    event_url = SerializerMethodField()
    get_event_url = hyperlinked_field_method('event')

    class Meta:
        model = Mutation
        fields = '__all__'
