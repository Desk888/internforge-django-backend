from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from apps.jobs.models import Job
from apps.companies.models import Company
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.search.models import SearchLog
from apps.search.serializers import SearchLogSerializer

class isAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class SearchLogViewSet(viewsets.ModelViewSet):
    queryset = SearchLog.objects.all()
    serializer_class = SearchLogSerializer
    permission_classes = [permissions.IsAuthenticated, isAdminUser]
    
    def get_queryset(self):
        return SearchLog.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_searches(self, request):
        searches = self.get_queryset()
        serializer = self.get_serializer(searches, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def log_search(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    
class PerformSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Search query is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Perform search
        jobs = Job.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        companies = Company.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

        # Log search
        SearchLog.objects.create(
            user=request.user,
            query=query,
            results_count=jobs.count() + companies.count()
        )

        # Return results
        return Response({
            "jobs": [{"id": job.id, "title": job.title} for job in jobs],
            "companies": [{"id": company.id, "name": company.name} for company in companies],
        })