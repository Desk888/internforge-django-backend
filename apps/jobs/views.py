from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Job
from apps.skills.models import JobSkill
from .serializers import JobSerializer
from apps.skills.serializers import JobSkillSerializer
from apps.users.permissions import IsEmployer, IsAdmin
from apps.search.models import SearchLog
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.notifications.service import NotificationService
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import JobFilter
from rest_framework import serializers

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filterset_class = JobFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'company__name', 'location']
    ordering_fields = ['created_at', 'salary', 'title']
    ordering = ['-created_at']  # Default ordering
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsEmployer() | IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'company'):
            serializer.save(company=self.request.user.company)
        else:
            raise serializers.ValidationError("User does not have an associated company.")
        job = serializer.instance
        NotificationService.notify_new_job_posted(job)

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if self.action in ['update', 'partial_update', 'destroy']:
            if not request.user.is_staff and obj.company != request.user.company:
                self.permission_denied(request)

class JobSkillViewSet(viewsets.ModelViewSet):
    queryset = JobSkill.objects.all()
    serializer_class = JobSkillSerializer
    permission_classes = [IsAuthenticated]
    
class JobSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Please provide a search query"}, status=400)

        search_vector = SearchVector('title', weight='A') + \
                        SearchVector('company_name', weight='B') + \
                        SearchVector('description', weight='C') + \
                        SearchVector('requirements', weight='C') + \
                        SearchVector('location', weight='D')

        search_query = SearchQuery(query, config='english')
        search_rank = SearchRank(search_vector, search_query)

        jobs = Job.objects.annotate(
            rank=search_rank
        ).filter(rank__gte=0.1).order_by('-rank')

        SearchLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            query=query,
            results_count=len(jobs)
        )

        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)