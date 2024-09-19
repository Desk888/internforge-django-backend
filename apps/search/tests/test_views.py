from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.search.models import SearchLog
from apps.users.models import User
from apps.jobs.models import Job
from apps.companies.models import Company

class SearchLogViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.client.force_authenticate(user=self.admin_user)
        self.search_log_data = {
            'query': 'python developer',
            'results_count': 5
        }

    def test_create_search_log(self):
        url = reverse('search-log-list')
        response = self.client.post(url, self.search_log_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SearchLog.objects.count(), 1)
        self.assertEqual(SearchLog.objects.get().query, 'python developer')

    def test_list_search_logs(self):
        SearchLog.objects.create(user=self.admin_user, **self.search_log_data)
        url = reverse('search-log-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_search_log(self):
        search_log = SearchLog.objects.create(user=self.admin_user, **self.search_log_data)
        url = reverse('search-log-detail', args=[search_log.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['query'], 'python developer')

class PerformSearchViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.company = Company.objects.create(company_name='Test Company')
        self.job = Job.objects.create(
            company=self.company,
            title='Python Developer',
            description='We are looking for a Python developer'
        )

    def test_perform_search(self):
        url = reverse('perform-search')
        response = self.client.get(url, {'q': 'Python'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('jobs', response.data)
        self.assertIn('companies', response.data)
        self.assertEqual(len(response.data['jobs']), 1)
        self.assertEqual(SearchLog.objects.count(), 1)

    def test_perform_search_no_results(self):
        url = reverse('perform-search')
        response = self.client.get(url, {'q': 'Java'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['jobs']), 0)
        self.assertEqual(len(response.data['companies']), 0)
        self.assertEqual(SearchLog.objects.count(), 1)

    def test_perform_search_missing_query(self):
        url = reverse('perform-search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)