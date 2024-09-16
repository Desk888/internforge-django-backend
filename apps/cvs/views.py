from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.cvs.models import CV
from apps.cvs.serializers import CVSerializer

class CVViewSet(viewsets.ModelViewSet):
    queryset = CV.objects.all()
    serializer_class = CVSerializer
    permission_classes = [IsAuthenticated]