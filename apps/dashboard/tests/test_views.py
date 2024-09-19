from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User
from apps.companies.models import Company
from apps.jobs.models import Job
from apps.applications.models import Application
from django.utils import timezone

class DashboardViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.job_seeker = User.objects.create_user(
            email='jobseeker@example.com',
            password='testpass123',
            user_type='JOB_SEEKER'
        )
        self.employer = User.objects.create_user(
            email='employer@example.com',
            password='testpass123',
            user_type='EMPLOYER'
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.company = Company.objects.create(
            company_name='Test Company',
            user=self.employer
        )
        self.job = Job.objects.create(
            company=self.company,
            title='Software Developer',
            description='A great job opportunity',
            application_deadline=timezone.now().date() + timezone.timedelta(days=30)
        )
        self.application = Application.objects.create(
            user=self.job_seeker,
            job=self.job
        )

    def test_job_seeker_dashboard(self):
        self.client.force_authenticate(user=self.job_seeker)
        url = reverse('job-seeker-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_applications', response.data)
        self.assertIn('pending_applications', response.data)
        self.assertIn('accepted_applications', response.data)
        self.assertIn('rejected_applications', response.data)
        self.assertIn('recent_applications', response.data)
        self.assertIn('recommended_jobs', response.data)

    def test_employer_dashboard(self):
        self.client.force_authenticate(user=self.employer)
        url = reverse('employer-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_jobs_posted', response.data)
        self.assertIn('active_jobs', response.data)
        self.assertIn('total_applications', response.data)
        self.assertIn('applications_by_status', response.data)
        self.assertIn('recent_applications', response.data)

    def test_admin_dashboard(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('admin-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_users', response.data)
        self.assertIn('total_companies', response.data)
        self.assertIn('total_jobs', response.data)
        self.assertIn('total_applications', response.data)
        self.assertIn('users_by_type', response.data)
        self.assertIn('jobs_by_status', response.data)
        self.assertIn('applications_by_status', response.data)

    def test_unauthorized_access(self):
        # Test job seeker accessing employer dashboard
        self.client.force_authenticate(user=self.job_seeker)
        url = reverse('employer-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test employer accessing admin dashboard
        self.client.force_authenticate(user=self.employer)
        url = reverse('admin-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)