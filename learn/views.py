from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

  
class NotesViewSet(ModelViewSet):
    queryset = Note.objects.all()
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return NoteReadSerialier
        return NoteSerializer
    
class TestsViewSet(ModelViewSet):
    queryset = Test.objects.all()
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return TestReadSerialier
        return TestSerializer

class GradesViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return GradeReadSerialier
        return GradeSerializer