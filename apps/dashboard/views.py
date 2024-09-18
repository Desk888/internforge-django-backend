from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import Count, Q
from apps.jobs.models import Job
from apps.applications.models import Application
from apps.users.models import User
from apps.companies.models import Company
from .permissions import IsJobSeeker, IsEmployer

class JobSeekerDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def get(self, request):
        user = request.user
        applied_jobs = Application.objects.filter(user=user).select_related('job')
        
        recommended_jobs = Job.objects.filter(
            status='OPEN'
        ).exclude(
            id__in=applied_jobs.values('job_id')
        )[:5]
        
        dashboard_data = {
            'total_applications': applied_jobs.count(),
            'pending_applications': applied_jobs.filter(status='PENDING').count(),
            'accepted_applications': applied_jobs.filter(status='ACCEPTED').count(),
            'rejected_applications': applied_jobs.filter(status='REJECTED').count(),
            'recent_applications': applied_jobs.order_by('-submitted_at')[:5].values('job__title', 'status', 'submitted_at'),
            'recommended_jobs': list(recommended_jobs.values('id', 'title', 'company__name'))
        }
        
        return Response(dashboard_data)

class EmployerDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def get(self, request):
        user = request.user
        try:
            company = user.company
        except Company.DoesNotExist:
            return Response({"error": "No company associated with this user"}, status=400)
        
        posted_jobs = Job.objects.filter(company=company)
        applications = Application.objects.filter(job__company=company)
        
        dashboard_data = {
            'total_jobs_posted': posted_jobs.count(),
            'active_jobs': posted_jobs.filter(status='OPEN').count(),
            'total_applications': applications.count(),
            'applications_by_status': applications.values('status').annotate(count=Count('status')),
            'recent_applications': applications.order_by('-submitted_at')[:5].values(
                'job__title', 'user__email', 'status', 'submitted_at'
            ),
        }
        
        return Response(dashboard_data)

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.user_type == 'ADMIN':
            raise PermissionDenied("You do not have permission to view this dashboard")
        
        dashboard_data = {
            'total_users': User.objects.count(),
            'total_companies': Company.objects.count(),
            'total_jobs': Job.objects.count(),
            'total_applications': Application.objects.count(),
            'users_by_type': User.objects.values('user_type').annotate(count=Count('user_type')),
            'jobs_by_status': Job.objects.values('status').annotate(count=Count('status')),
            'applications_by_status': Application.objects.values('status').annotate(count=Count('status')),
        }
        
        return Response(dashboard_data)