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
    