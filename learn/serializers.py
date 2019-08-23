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
    notes = SlugRelatedField(slug_field="uuid", many=True, queryset=Note.objects.all())
    class Meta:
        model = Test
        fields = '__all__'

class TestReadSerializer(ModelSerializer):
    notes = NoteReadSerializer(read_only=True, many=True)
    class Meta:
        model = Test
        fields = '__all__'

class GradeSerializer(ModelSerializer):
    test = SlugRelatedField(slug_field="uuid", queryset=Test.objects.all())
    class Meta:
        model = Grade
        fields = '__all__'

class GradeReadSerializer(ModelSerializer):
    test = TestReadSerializer(read_only=True)
    class Meta:
        model = Grade
        fields = '__all__'