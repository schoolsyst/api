from rest_framework.serializers import *
from rest_framework.permissions import *
from .models import *

class DefaultSettingSerializer(ModelSerializer):
    class Meta:
        model = DefaultSetting
        fields = '__all__'

class SettingSerializer(ModelSerializer):
    setting = SlugRelatedField(slug_field='key', queryset=DefaultSetting.objects.all())

    class Meta:
        model = Setting
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        
        return Setting.objects.create(**validated_data)

class SettingReadSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    setting = DefaultSettingSerializer(read_only=True)
    class Meta:
        model = Setting
        fields = '__all__'


class SubjectSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())        

    class Meta:
        model = Subject
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Subject.objects.create(**validated_data)


