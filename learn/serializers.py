from rest_framework.serializers import *
from .models import *
from common.serializers import *
from common.models import *

class NotionSerializer(ModelSerializer):
    subject = SlugRelatedField(slug_field='slug', queryset=Subject.objects.all())
    class Meta:
        model = Notion
        fields = '__all__'

class NotionReadSerialier(ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    class Meta:
        model = Notion
        fields = '__all__'

class TestSerializer(ModelSerializer):
    notions = SlugRelatedField(slug_field='slug', many=True, queryset=Notion.objects.all())
    class Meta:
        model = Test
        fields = '__all__'

class TestReadSerialier(ModelSerializer):
    notions = NotionSerializer(read_only=True, many=True)
    class Meta:
        model = Test
        fields = '__all__'

class GradeSerializer(ModelSerializer):
    tests = PrimaryKeyRelatedField(many=True, queryset=Test.objects.all())
    class Meta:
        model = Grade
        fields = '__all__'

class GradeReadSerialier(ModelSerializer):
    tests = TestSerializer(read_only=True, many=True)
    class Meta:
        model = Grade
        fields = '__all__'

class NoteSerializer(ModelSerializer):
    notion = SlugRelatedField(slug_field='slug', queryset=Notion.objects.all())
    class Meta:
        model = Note
        fields = '__all__'

class NoteReadSerialier(ModelSerializer):
    notion = NotionSerializer(read_only=True)
    class Meta:
        model = Note
        fields = '__all__'

