from django.test import TestCase
from apps.companies.models import Company
from apps.users.models import User

class CompanyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            user_type='EMPLOYER'
        )
        self.company_data = {
            'company_name': 'Test Company',
            'description': 'A test company',
            'website': 'https://testcompany.com',
            'address_line_one': '123 Test St',
            'city': 'Test City',
            'country': 'Test Country',
            'postcode': '12345',
            'industry': 'Technology',
            'user': self.user
        }

    def test_create_company(self):
        company = Company.objects.create(**self.company_data)
        self.assertEqual(company.company_name, self.company_data['company_name'])
        self.assertEqual(company.user, self.user)

    def test_company_str_method(self):
        company = Company.objects.create(**self.company_data)
        self.assertEqual(str(company), self.company_data['company_name'])

    def test_company_status(self):
        company = Company.objects.create(**self.company_data)
        self.assertEqual(company.company_status, 'ACTIVE')
        
        company.company_status = 'INACTIVE'
        company.save()
        self.assertEqual(company.company_status, 'INACTIVE')

    def test_company_employee_count(self):
        company = Company.objects.create(**self.company_data)
        company.employee_count = 100
        company.save()
        self.assertEqual(company.employee_count, 100)

    def test_company_founded_year(self):
        company = Company.objects.create(**self.company_data)
        company.founded_year = 2000
        company.save()
        self.assertEqual(company.founded_year, 2000)