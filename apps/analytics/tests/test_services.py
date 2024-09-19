from django.test import TestCase
from django.utils import timezone
from apps.analytics.models import Event, DailyStats
from apps.analytics.service import AnalyticsService
from apps.users.models import User
from apps.jobs.models import Job
from apps.companies.models import Company
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class AnalyticsServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.company = Company.objects.create(company_name='Test Company')
        self.job = Job.objects.create(
            company=self.company,
            title='Software Developer'
        )

    def test_track_event(self):
        AnalyticsService.track_event('job_view', user=self.user, obj=self.job)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertEqual(event.event_type, 'job_view')
        self.assertEqual(event.user, self.user)
        self.assertEqual(event.content_object, self.job)

    def test_track_event_updates_daily_stats(self):
        AnalyticsService.track_event('job_view', user=self.user, obj=self.job)
        self.assertEqual(DailyStats.objects.count(), 1)
        stats = DailyStats.objects.first()
        self.assertEqual(stats.job_views, 1)

    def test_track_active_user(self):
        AnalyticsService.track_active_user(self.user)
        self.assertEqual(DailyStats.objects.count(), 1)
        stats = DailyStats.objects.first()
        self.assertEqual(stats.active_users, 1)

    def test_multiple_events(self):
        AnalyticsService.track_event('job_view', user=self.user, obj=self.job)
        AnalyticsService.track_event('job_application', user=self.user, obj=self.job)
        AnalyticsService.track_event('search_query', user=self.user)
        
        self.assertEqual(Event.objects.count(), 3)
        stats = DailyStats.objects.first()
        self.assertEqual(stats.job_views, 1)
        self.assertEqual(stats.job_applications, 1)
        self.assertEqual(stats.search_queries, 1)

class AnalyticsTasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.company = Company.objects.create(company_name='Test Company')
        self.job = Job.objects.create(
            company=self.company,
            title='Software Developer'
        )

    def test_process_daily_stats(self):
        # Create some events
        for _ in range(5):
            AnalyticsService.track_event('job_view', user=self.user, obj=self.job)
        for _ in range(3):
            AnalyticsService.track_event('job_application', user=self.user, obj=self.job)
        
        # Run the task
        from apps.analytics.tasks import process_daily_stats
        process_daily_stats()

        # Check the results
        stats = DailyStats.objects.first()
        self.assertEqual(stats.job_views, 5)
        self.assertEqual(stats.job_applications, 3)
        self.assertEqual(stats.active_users, 1)

class AnalyticsSummaryViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.client.force_authenticate(user=self.admin_user)

        # Create some dummy data
        today = timezone.now().date()
        for i in range(30):
            DailyStats.objects.create(
                date=today - timezone.timedelta(days=i),
                job_views=i*10,
                job_applications=i*2,
                new_users=i,
                active_users=i*5,
                search_queries=i*20
            )

    def test_analytics_summary(self):
        url = reverse('analytics-summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_job_views', response.data)
        self.assertIn('total_applications', response.data)
        self.assertIn('total_new_users', response.data)
        self.assertIn('total_active_users', response.data)
        self.assertIn('total_search_queries', response.data)

    def test_analytics_summary_unauthorized(self):
        self.client.logout()
        url = reverse('analytics-summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)