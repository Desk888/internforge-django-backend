from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import DailyStats

class AnalyticsSummaryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        stats = DailyStats.objects.filter(date__range=[start_date, end_date]).aggregate(
            total_job_views=Sum('job_views'),
            total_applications=Sum('job_applications'),
            total_new_users=Sum('new_users'),
            total_active_users=Sum('active_users'),
            total_search_queries=Sum('search_queries')
        )
        
        return Response(stats)