from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import CV
from .serializers import CVSerializer

class CVPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CVViewSet(viewsets.ModelViewSet):
    serializer_class = CVSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
    pagination_class = CVPagination

    def get_queryset(self):
        return CV.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def set_active(self, request, pk=None):
        cv = self.get_object()
        CV.objects.filter(user=request.user).update(is_active=False)
        cv.is_active = True
        cv.save()
        return Response({'status': 'CV set as active'})

    def destroy(self, request, *args, **kwargs):
        cv = self.get_object()
        if cv.is_active:
            return Response({"detail": "Cannot delete the active CV."}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)