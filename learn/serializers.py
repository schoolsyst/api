from rest_framework.serializers import *
from .models import *
from common.serializers import *
from common.models import *
from common.utils import hyperlinked_field_method


class NoteSerializer(ModelSerializer):
    """
    Serializer for Note objects
    with slug fields replacing nested relations,
    needed when POST, PUT or PATCH'ing data.
    """

    subject = SlugRelatedField(
        slug_field='uuid', queryset=Subject.objects.all())

    class Meta:
        model = Note
        fields = '__all__'


class NoteReadSerializer(ModelSerializer):
    """
    ReadSerializer for Note objects
    with nested + hyperlinked relation representations
    useful when GET'ing data.
    """

    subject = SubjectSerializer(read_only=True)
    subject_url = SerializerMethodField()
    get_subject_url = hyperlinked_field_method('subject')

    class Meta:
        model = Note
        fields = '__all__'
        lookup_field = 'uuid'


class LearndataSerializer(ModelSerializer):
    """
    Serializer for Learndata objects
    with slug fields replacing nested relations,
    needed when POST, PUT or PATCH'ing data.
    """

    subject = SlugRelatedField(
        slug_field='uuid',
        queryset=Subject.objects.all()
    )
    notes = SlugRelatedField(
        slug_field='uuid',
        queryset=Note.objects.all(),
        allow_null=True,
        many=True
    )

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
    notes = NoteReadSerializer(read_only=True, many=True)

    subject_url = SerializerMethodField()
    get_subject_url = hyperlinked_field_method('subject')

    class Meta:
        model = Learndata
        fields = '__all__'
