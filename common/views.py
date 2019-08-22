from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.renderers import JSONRenderer
from .models import *
from .serializers import *


class DefaultSettingViewSet(ModelViewSet):
    lookup_field = 'key'
    queryset = DefaultSetting.objects.all()
    serializer_class = DefaultSettingSerializer


class SettingsViewSet(ModelViewSet):
    lookup_field = 'setting__key'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return SettingReadSerializer
        return SettingSerializer

    def get_queryset(self):
        return Setting.objects.filter(user__pk=self.request.user.id)


class SubjectsViewSet(ModelViewSet):
    lookup_field = 'uuid'
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return Subject.objects.filter(user__pk=self.request.user.id)
