from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.jobs.models import Job
from apps.companies.models import Company
from apps.users.models import User
from django.utils import timezone

class JobViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            user_type='EMPLOYER'
        )
        self.company = Company.objects.create(
            company_name='Test Company',
            user=self.user
        )
        self.client.force_authenticate(user=self.user)
        self.job_data = {
            'company': self.company.pk,
            'title': 'Software Developer',
            'description': 'A great job opportunity',
            'location': 'Remote',
            'contract_type': 'FULL_TIME',
            'requirements': 'Python, Django',
            'salary': '50000-70000',
            'application_deadline': (timezone.now().date() + timezone.timedelta(days=30)).isoformat(),
            'number_of_openings': 2,
            'is_remote': True,
            'experience_level': 'MID'
        }

    def test_create_job(self):
        url = reverse('job-list')
        response = self.client.post(url, self.job_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 1)
        self.assertEqual(Job.objects.get().title, 'Software Developer')

    def test_retrieve_job(self):
        job = Job.objects.create(company=self.company, **self.job_data)
        url = reverse('job-detail', args=[job.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Software Developer')

    def test_update_job(self):
        job = Job.objects.create(company=self.company, **self.job_data)
        url = reverse('job-detail', args=[job.pk])
        updated_data = {'title': 'Senior Software Developer'}
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Job.objects.get().title, 'Senior Software Developer')

    def test_delete_job(self):
        job = Job.objects.create(company=self.company, **self.job_data)
        url = reverse('job-detail', args=[job.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Job.objects.count(), 0)

    def test_list_jobs(self):
        Job.objects.create(company=self.company, **self.job_data)
        url = reverse('job-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_jobs(self):
        Job.objects.create(company=self.company, **self.job_data)
        url = reverse('job-list')
        response = self.client.get(url, {'location': 'Remote'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(url, {'location': 'Office'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_search_jobs(self):
        Job.objects.create(company=self.company, **self.job_data)
        url = reverse('job-list')
        response = self.client.get(url, {'search': 'Software Developer'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(url, {'search': 'Nonexistent Job'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

class JobSearchViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.company = Company.objects.create(company_name='Test Company', user=self.user)
        self.job = Job.objects.create(
            company=self.company,
            title='Software Developer',
            description='Python developer needed',
            location='Remote'
        )

    def test_job_search(self):
        url = reverse('job-search')
        response = self.client.get(url, {'q': 'Python'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Software Developer')

        response = self.client.get(url, {'q': 'Java'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)