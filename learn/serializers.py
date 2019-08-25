from rest_framework.serializers import *
from .models import *
from common.serializers import *
from common.models import *

class NoteSerializer(ModelSerializer):
    subject = SlugRelatedField(slug_field='slug', queryset=Subject.objects.all())
    class Meta:
        model = Note
        fields = '__all__'

class NoteReadSerializer(ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    class Meta:
        model = Note
        fields = '__all__'
        lookup_field = 'uuid'
        
class TestSerializer(ModelSerializer):
    notes   = SlugRelatedField(slug_field="uuid", many=True, queryset=Note.objects.all())
    subject = SlugRelatedField(slug_field="slug", queryset=Subject.objects.all())
    class Meta:
        model = Test
        fields = '__all__'

class GradeReadSerializer(ModelSerializer):
    class Meta:
        model = Grade
        exclude = ('test',)

class TestReadSerializer(ModelSerializer):
    notes   = NoteReadSerializer(read_only=True, many=True)
    subject = SubjectSerializer(read_only=True)
    grades  = GradeReadSerializer(read_only=True, many=True)
    class Meta:
        model = Test
        fields = '__all__'

class GradeSerializer(ModelSerializer):
    test = SlugRelatedField(slug_field="uuid", queryset=Test.objects.all())
    class Meta:
        model = Grade
        fields = '__all__'