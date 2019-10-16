from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from .models import *
from .serializers import *


class SettingDefinitionViewSet(ModelViewSet):
    lookup_field = 'key'
    queryset = SettingDefinition.objects.all()
    serializer_class = SettingDefinitionSerializer


class SettingsViewSet(ModelViewSet):
    lookup_field = 'setting__key'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return SettingReadSerializer
        return SettingSerializer

    def get_queryset(self):
        return Setting.objects.filter(user__id=self.request.user.id)


class SubjectsViewSet(ModelViewSet):
    lookup_field = 'uuid'
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return Subject.objects.filter(user__pk=self.request.user.id)


class UserViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return UserReadSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(pk=self.request.user.id)


class CurrentUserViewSet(ModelViewSet):
    """
    API endpoint that allows the current user to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserCurrentSerializer

    def get_object(self):
        return self.request.user
