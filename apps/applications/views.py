from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.applications.models import Application
from apps.applications.serializers import ApplicationSerializer
from apps.users.permissions import IsJobSeeker, IsEmployer, IsAdmin
from apps.notifications.service import NotificationService
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ApplicationFilter


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ApplicationFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['submitted_at', 'last_updated', 'created_at']
    ordering = ['-submitted_at']
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsJobSeeker]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, (IsJobSeeker | IsEmployer | IsAdmin)]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Application.objects.all()
        elif user.user_type == 'EMPLOYER':
            return Application.objects.filter(job__company__user=user)
        else:
            return Application.objects.filter(user=user)

    def perform_create(self, serializer):
        application = serializer.save(user=self.request.user, status='PENDING')
        NotificationService.notify_application_received(application)

    def perform_update(self, serializer):
        old_status = self.get_object().status
        application = serializer.save()
        if application.status != old_status:
            NotificationService.notify_application_status_change(application)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        if 'status' in serializer.validated_data:
            new_status = serializer.validated_data['status']
            if not self._is_valid_status_transition(instance.status, new_status):
                return Response({"detail": "Invalid status transition."}, status=status.HTTP_400_BAD_REQUEST)
            
            if request.user.is_staff or (request.user.user_type == 'EMPLOYER' and instance.job.company.user == request.user):
                self.perform_update(serializer)
            else:
                return Response({"detail": "You don't have permission to update the status."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"detail": "Only status updates are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    def _is_valid_status_transition(self, old_status, new_status):
        valid_transitions = {
            'PENDING': ['REVIEWED', 'REJECTED', 'ACCEPTED'],
            'REVIEWED': ['REJECTED', 'ACCEPTED'],
            'REJECTED': [],
            'ACCEPTED': ['REJECTED']
        }
        return new_status in valid_transitions.get(old_status, [])
