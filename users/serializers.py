from rest_framework.serializers import *
from .models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'password', 'username', 'email')
        
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserReadSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_login', 'date_joined', 'email', 'username', 'is_staff')


class CurrentUserSerializer(HyperlinkedModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.save()

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'ip_address', 'is_staff', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'url': {'lookup_field': 'id'}
        }
        read_only_fields = ('id', 'is_staff', 'ip_address')
