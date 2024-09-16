from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Job
from apps.skills.models import JobSkill
from .serializers import JobSerializer
from apps.skills.serializers import JobSkillSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

class JobSkillViewSet(viewsets.ModelViewSet):
    queryset = JobSkill.objects.all()
    serializer_class = JobSkillSerializer
    permission_classes = [IsAuthenticated]