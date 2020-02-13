from rest_framework.serializers import *
from rest_framework import serializers
from common.models import Subject
from common.serializers import *
from .models import *
import schedule.models



class EventSerializer(ModelSerializer):
    subject = SlugRelatedField(
        slug_field='uuid', queryset=Subject.objects.all())

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
    subject = SlugRelatedField(slug_field='uuid', queryset=Subject.objects.all())

    class Meta:
        model = Mutation
        fields = '__all__'


class MutationReadSerializer(ModelSerializer):
    event = EventReadSerializer(read_only=True)
    event_url = SerializerMethodField()
    get_event_url = hyperlinked_field_method('event')

    subject = SubjectSerializer(read_only=True)
    subject_url = SerializerMethodField()
    get_subject_url = hyperlinked_field_method('subject')
    
    type = ReadOnlyField()

    class Meta:
        model = Mutation
        fields = '__all__'

class CourseReadSerializer(Serializer):
    subject = SubjectSerializer()
    uuid = serializers.UUIDField()
    room = serializers.CharField(max_length=300)
    week_type = serializers.ChoiceField(choices=schedule.models.WEEK_TYPES)
    day = serializers.ChoiceField(choices=schedule.models.WEEK_DAYS)
    mutation = MutationReadSerializer()

    # This is the difference w/ Event:
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
