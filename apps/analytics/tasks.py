from project.celery import app
from django.db.models import Count
from django.utils import timezone
from .models import Event, DailyStats

@app.task
def process_daily_stats():
    today = timezone.now().date()
    stats, _ = DailyStats.objects.get_or_create(date=today)
    
    events = Event.objects.filter(timestamp__date=today)
    stats.job_views = events.filter(event_type='job_view').count()
    stats.job_applications = events.filter(event_type='job_application').count()
    stats.new_users = events.filter(event_type='user_registration').count()
    stats.search_queries = events.filter(event_type='search_query').count()
    
    stats.active_users = events.values('user').distinct().count()
    
    stats.save()