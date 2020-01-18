from rest_framework.serializers import *
from rest_framework.permissions import *
from .models import *
from common.utils import hyperlinked_field_method

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

class OffdaySerializer(ModelSerializer):
    class Meta:
        model = Offday
        fields = ('start', 'end')

class UserSettingsSerializer(ModelSerializer):
    class Meta:
        model = UserSettings
        fields = (
            'year_start',
            'offdays',
            'trimester_2_start',
            'trimester_3_start',
            'year_end',
            'theme',
            'show_completed_exercises',
            'grades_unit',
            'grades_default_weight',
        )


class UserSerializer(ModelSerializer):
    settings = UserSettingsSerializer()
    
    class Meta:
        model = User
        fields = ('id', 'password', 'username', 'email', 'settings')

    def create(self, validated_data):
        user = User(
            **{**validated_data, 'settings': None},
            ip_address=self.context['request'].META.get('REMOTE_ADDR', None)
        )
        user.email = validated_data['email']
        user.settings = None
        user.set_password(validated_data['password'])
        print(user)
        user.save()
        settings = UserSettings.objects.create(user=user, **validated_data['settings'])
        user.settings = settings
        user.save()
        return user


class UserReadSerializer(ModelSerializer):
    settings = UserSettingsSerializer()
    
    class Meta:
        model = User
        fields = ('id', 'last_login', 'date_joined', 'email',
                  'username', 'is_staff', 'setup_step',
                  'remaining_daily_github_issues', 'settings')


class UserCurrentSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        if 'password' in validated_data.keys():
            instance.set_password(validated_data['password'])
        if 'last_login' in validated_data.keys():
            instance.last_login = validated_data['last_login']
        if 'ip_address' in validated_data.keys():
            instance.last_login = validated_data['ip_address']
        if 'settings' in validated_data.keys():
            instance.settings = UserSettings(**validated_data['settings'])
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ('id', 'last_login', 'date_joined', 'email',
                  'username', 'is_staff', 'setup_step',
                  'ip_address', 'remaining_daily_github_issues')
        extra_kwargs = {
            'password': {'write_only': True},
            'url': {'lookup_field': 'id'}
        }
        read_only_fields = ('id', 'is_staff')
