from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.applications.models import Application
from apps.users.models import User
from apps.companies.models import Company
from apps.jobs.models import Job
from apps.cvs.models import CV
from django.utils import timezone

class ApplicationViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.company = Company.objects.create(
            company_name='Test Company',
            user=self.user
        )
        self.job = Job.objects.create(
            company=self.company,
            title='Software Developer',
            description='A great job opportunity',
            application_deadline=timezone.now().date() + timezone.timedelta(days=30)
        )
        self.cv = CV.objects.create(
            user=self.user,
            file_name='test_cv.pdf',
            file_path='path/to/test_cv.pdf'
        )
        self.client.force_authenticate(user=self.user)
        self.application_data = {
            'job': self.job.pk,
            'cv': self.cv.pk,
            'cover_letter': 'I am very interested in this position.'
        }

    def test_create_application(self):
        url = reverse('application-list')
        response = self.client.post(url, self.application_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(Application.objects.get().user, self.user)

    def test_retrieve_application(self):
        application = Application.objects.create(user=self.user, job=self.job, cv=self.cv)
        url = reverse('application-detail', args=[application.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['job'], self.job.pk)

    def test_update_application(self):
        application = Application.objects.create(user=self.user, job=self.job, cv=self.cv)
        url = reverse('application-detail', args=[application.pk])
        updated_data = {'cover_letter': 'Updated cover letter'}
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Application.objects.get().cover_letter, 'Updated cover letter')

    def test_delete_application(self):
        application = Application.objects.create(user=self.user, job=self.job, cv=self.cv)
        url = reverse('application-detail', args=[application.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Application.objects.count(), 0)

    def test_list_applications(self):
        Application.objects.create(user=self.user, job=self.job, cv=self.cv)
        url = reverse('application-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_applications(self):
        Application.objects.create(user=self.user, job=self.job, cv=self.cv, status='PENDING')
        url = reverse('application-list')
        response = self.client.get(url, {'status': 'PENDING'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(url, {'status': 'ACCEPTED'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_update_application_status(self):
        application = Application.objects.create(user=self.user, job=self.job, cv=self.cv, status='PENDING')
        url = reverse('application-detail', args=[application.pk])
        updated_data = {'status': 'ACCEPTED'}
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Application.objects.get().status, 'ACCEPTED')

    def test_create_duplicate_application(self):
        Application.objects.create(user=self.user, job=self.job, cv=self.cv)
        url = reverse('application-list')
        response = self.client.post(url, self.application_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Application.objects.count(), 1)

    def test_application_for_closed_job(self):
        self.job.status = 'CLOSED'
        self.job.save()
        url = reverse('application-list')
        response = self.client.post(url, self.application_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Application.objects.count(), 0)

class ApplicationAnalyticsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.company = Company.objects.create(
            company_name='Test Company',
            user=self.user
        )
        self.job = Job.objects.create(
            company=self.company,
            title='Software Developer',
            description='A great job opportunity',
            application_deadline=timezone.now().date() + timezone.timedelta(days=30)
        )
        self.client.force_authenticate(user=self.user)

    def test_application_analytics(self):
        # Create some applications
        for _ in range(5):
            Application.objects.create(user=self.user, job=self.job)

        # Test the analytics endpoint
        url = reverse('application-analytics', args=[self.job.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_applications'], 5)
        self.assertIn('applications_by_status', response.data)
        self.assertIn('applications_over_time', response.data)