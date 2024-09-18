from .models import Event, DailyStats
from django.utils import timezone
from django.db.models import F

class AnalyticsService:
    @staticmethod
    def track_event(event_type, user=None, obj=None, **extra_data):
        Event.objects.create(
            user=user,
            event_type=event_type,
            content_object=obj,
            data=extra_data
        )
        
        today = timezone.now().date()
        stats, _ = DailyStats.objects.get_or_create(date=today)
        
        if event_type == 'job_view':
            stats.job_views = F('job_views') + 1
        elif event_type == 'job_application':
            stats.job_applications = F('job_applications') + 1
        elif event_type == 'user_registration':
            stats.new_users = F('new_users') + 1
        elif event_type == 'search_query':
            stats.search_queries = F('search_queries') + 1
        
        stats.save()

    @staticmethod
    def track_active_user(user):
        today = timezone.now().date()
        stats, _ = DailyStats.objects.get_or_create(date=today)
        stats.active_users = F('active_users') + 1
        stats.save()