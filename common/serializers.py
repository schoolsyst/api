from rest_framework.serializers import *
from rest_framework.permissions import *
from .models import *
from common.utils import hyperlinked_field_method


class SettingDefinitionSerializer(ModelSerializer):
    class Meta:
        model = SettingDefinition
        fields = '__all__'


class SettingSerializer(ModelSerializer):
    setting = SlugRelatedField(
        slug_field='key', queryset=SettingDefinition.objects.all())

    class Meta:
        model = Setting
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        return Setting.objects.create(**validated_data)


class SettingReadSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    setting = SettingDefinitionSerializer(read_only=True)
    setting_url = SerializerMethodField()
    get_setting_url = hyperlinked_field_method(
        'setting', 'key', name='settings-definitions')

    class Meta:
        model = Setting
        fields = '__all__'


class SubjectSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    user_url = SerializerMethodField()
    get_user_url = hyperlinked_field_method('user', 'id')

    class Meta:
        model = Subject
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Subject.objects.create(**validated_data)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'password', 'username', 'email')

    def create(self, validated_data):
        user = User(
            **validated_data,
            ip_address=self.context['request'].META.get('REMOTE_ADDR', None)
        )
        user.email = validated_data['email']
        user.save()
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserReadSerializer(ModelSerializer):
    is_setup = SerializerMethodField('is_setup')

    def get_is_setup(self, obj):
        return self.is_setup()

    class Meta:
        model = User
        fields = ('id', 'last_login', 'date_joined', 'email',
                  'username', 'is_staff')


class UserCurrentSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        if 'password' in validated_data.keys():
            instance.set_password(validated_data['password'])
        if 'last_login' in validated_data.keys():
            instance.last_login = validated_data['last_login']
        if 'ip_address' in validated_data.keys():
            instance.last_login = validated_data['ip_address']
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'ip_address', 'is_staff', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'url': {'lookup_field': 'id'}
        }
        read_only_fields = ('id', 'is_staff')
