from rest_framework.serializers import *
from .models import *
from common.serializers import *
from common.models import *
from common.utils import hyperlinked_field_method


class HomeworkSerializer(ModelSerializer):
    """
    Serializer for Homework objects
    with slug fields replacing nested relations,
    needed when POST, PUT or PATCH'ing data.
    """
    subject = SlugRelatedField(
        slug_field='uuid',
        queryset=Subject.objects.all(),
    )

    class Meta:
        model = Homework
        fields = '__all__'


class HomeworkReadSerializer(ModelSerializer):
    """
    ReadSerializer for Homework objects
    with nested relation representations
    useful when GET'ing data.
    """
    subject = SubjectSerializer(read_only=True)
    subject_url = SerializerMethodField()
    get_subject_url = hyperlinked_field_method('subject')

    class Meta:
        model = Homework
        fields = '__all__'
        lookup_field = 'uuid'


class GradeSerializer(ModelSerializer):
    """
    Serializer for Grade objects
    with slug fields replacing nested relations,
    needed when POST, PUT or PATCH'ing data.
    """
    subject = SlugRelatedField(
        slug_field="uuid", queryset=Subject.objects.all())

    class Meta:
        model = Grade
        fields = '__all__'


class GradeReadSerializer(ModelSerializer):
    """
    ReadSerializer for Grade objects
    with nested relation representations
    useful when GET'ing data.
    """
    subject = SubjectSerializer(read_only=True)
    subject_url = SerializerMethodField()
    get_subject_url  = hyperlinked_field_method('subject')

    class Meta:
        model = Grade
        fields = '__all__'
        lookup_field = 'uuid'
