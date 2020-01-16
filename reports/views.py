from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import *
from .serializers import *

# Create your views here.
class ReportsViewSet(ModelViewSet):
  lookup_field = 'uuid'

  def get_serializer_class(self):
    if self.request.method in ['GET']:
      return ReportReadSerializer
    return ReportSerializer

  def get_queryset(self):
    return Report.objects.filter(user__id=self.request.user.id)
