from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.search.models import SearchLog
from apps.search.serializers import SearchLogSerializer

class SearchLogViewSet(viewsets.ModelViewSet):
    queryset = SearchLog.objects.all()
    serializer_class = SearchLogSerializer
    permission_classes = [IsAuthenticated]