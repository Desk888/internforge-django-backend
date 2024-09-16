from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.applications.models import Application
from apps.applications.serializers import ApplicationSerializer
from apps.users.permissions import IsJobSeeker, IsEmployer, IsAdmin

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsJobSeeker]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, (IsJobSeeker | IsEmployer | IsAdmin)]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='JOB_SEEKER').exists():
            return Application.objects.filter(user=user)
        elif user.groups.filter(name='EMPLOYER').exists():
            return Application.objects.filter(job__company=user.company)
        return Application.objects.all()  # For admin users

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if self.action in ['update', 'partial_update', 'destroy']:
            if request.user.groups.filter(name='JOB_SEEKER').exists() and obj.user != request.user:
                self.permission_denied(request)
            elif request.user.groups.filter(name='EMPLOYER').exists() and obj.job.company != request.user.company:
                self.permission_denied(request)
