from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.renderers import JSONRenderer
from .models import Setting, Subject
from .serializers import SettingSerializer, SubjectSerializer

class SettingsViewSet(ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    
class SubjectsViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Subject.objects.all()
        else:
            return Subject.objects.filter(user__pk=self.request.user.id)
    

#class SubjectList(ListCreateAPIView):
#    queryset = Subject.objects.all()
#    serializer_class = SubjectSerializer
#    def perform_create(self, serializer):
#        serializer.save(user=self.request.user)
#
#class SubjectDetail(RetrieveUpdateDestroyAPIView):
#    queryset = Subject.objects.all()
#    serializer_class = SubjectSerializer