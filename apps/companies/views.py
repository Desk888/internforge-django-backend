from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]