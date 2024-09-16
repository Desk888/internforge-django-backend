from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.applications.models import Application
from apps.applications.serializers import ApplicationSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]