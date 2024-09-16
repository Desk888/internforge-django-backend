from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.jobs.models import Job
from apps.jobs.serializers import JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]