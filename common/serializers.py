from rest_framework.serializers import *
from .models import *

class SettingSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())        

    class Meta:
        model = Setting
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Setting.objects.create(**validated_data)


class SubjectSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())        

    class Meta:
        model = Subject
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Subject.objects.create(**validated_data)


