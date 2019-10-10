from rest_framework.serializers import *
from .models import *
from common.serializers import *
from common.models import *


class LearndataSerializer(ModelSerializer):
    """
    Serializer for Learndata objects
    with slug fields replacing nested relations,
    needed when POST, PUT or PATCH'ing data.
    """

    subject = SlugRelatedField(
        slug_field='slug', queryset=Subject.objects.all())

    class Meta:
        model = Learndata
        fields = '__all__'


class LearndataReadSerializer(ModelSerializer):
    """
    ReadSerializer for Learndata objects
    with nested relation representations
    useful when GET'ing data.
    """

    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = Learndata
        fields = '__all__'


class NoteSerializer(ModelSerializer):
    """
    Serializer for Note objects
    with slug fields replacing nested relations,
    needed when POST, PUT or PATCH'ing data.
    """

    subject = SlugRelatedField(
        slug_field='slug', queryset=Subject.objects.all())
    learndata = SlugRelatedField(
        slug_field='uuid', queryset=Learndata.objects.all())

    class Meta:
        model = Note
        fields = '__all__'


class NoteReadSerializer(ModelSerializer):
    """
    ReadSerializer for Note objects
    with nested relation representations
    useful when GET'ing data.
    """

    subject = SubjectSerializer(read_only=True)
    learndata = LearndataReadSerializer(read_only=True)

    class Meta:
        model = Note
        fields = '__all__'
        lookup_field = 'uuid'
