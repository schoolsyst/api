from rest_framework.serializers import *
from .models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        #exclude = ('password',)
        
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    