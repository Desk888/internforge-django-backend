from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.companies.models import Company
from apps.users.models import User

class CompanyViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            user_type='EMPLOYER'
        )
        self.client.force_authenticate(user=self.user)
        self.company_data = {
            'company_name': 'Test Company',
            'description': 'A test company',
            'website': 'https://testcompany.com',
            'address_line_one': '123 Test St',
            'city': 'Test City',
            'country': 'Test Country',
            'postcode': '12345',
            'industry': 'Technology',
            'user': self.user.pk
        }

    def test_create_company(self):
        url = reverse('company-list')
        response = self.client.post(url, self.company_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().company_name, 'Test Company')

    def test_retrieve_company(self):
        company = Company.objects.create(**self.company_data)
        url = reverse('company-detail', args=[company.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['company_name'], 'Test Company')

    def test_update_company(self):
        company = Company.objects.create(**self.company_data)
        url = reverse('company-detail', args=[company.pk])
        updated_data = {'company_name': 'Updated Company'}
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.get().company_name, 'Updated Company')

    def test_delete_company(self):
        company = Company.objects.create(**self.company_data)
        url = reverse('company-detail', args=[company.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 0)

    def test_list_companies(self):
        Company.objects.create(**self.company_data)
        url = reverse('company-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_companies(self):
        Company.objects.create(**self.company_data)
        url = reverse('company-list')
        response = self.client.get(url, {'industry': 'Technology'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(url, {'industry': 'Finance'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_search_companies(self):
        Company.objects.create(**self.company_data)
        url = reverse('company-list')
        response = self.client.get(url, {'search': 'Test Company'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(url, {'search': 'Nonexistent Company'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)