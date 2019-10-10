from rest_framework.serializers import *
from .models import *
from common.serializers import *
from common.models import *


class Homeworkerializer(ModelSerializer):
    """
    Serializer for Homework objects
    with slug fields replacing nested relations,
    needed when POST, PUT or PATCH'ing data.
    """
    subject = SlugRelatedField(
        slug_field='slug',
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
    homework = SlugRelatedField(
        slug_field="uuid", queryset=Grade.objects.all(), allow_null=True)
    subject = SlugRelatedField(
        slug_field="slug", queryset=Subject.objects.all())

    class Meta:
        model = Grade
        fields = '__all__'


class GradeReadSerializer(ModelSerializer):
    """
    ReadSerializer for Grade objects
    with nested relation representations
    useful when GET'ing data.
    """
    homework = HomeworkReadSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = Grade
        fields = '__all__'
        lookup_field = 'uuid'
