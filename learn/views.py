from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

class NotionsViewSet(ModelViewSet):
    queryset = Notion.objects.all()
    serializer_class = NotionSerializer
    
class NotesViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    
class TestsViewSet(ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class GradesViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer