from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Job
from apps.skills.models import JobSkill
from .serializers import JobSerializer
from apps.skills.serializers import JobSkillSerializer
from apps.users.permissions import IsEmployer, IsAdmin

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, (IsEmployer | IsAdmin)]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
        
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, (IsEmployer | IsAdmin)]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if self.action in ['update', 'partial_update', 'destroy']:
            if not request.user.is_staff and obj.company != request.user.company:
                self.permission_denied(request)

class JobSkillViewSet(viewsets.ModelViewSet):
    queryset = JobSkill.objects.all()
    serializer_class = JobSkillSerializer
    permission_classes = [IsAuthenticated]