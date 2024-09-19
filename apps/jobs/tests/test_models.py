from django.test import TestCase
from apps.jobs.models import Job
from apps.companies.models import Company
from apps.users.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class JobModelTest(TestCase):
    def setUp(self):
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
        self.job_data = {
            'company': self.company,
            'title': 'Software Developer',
            'description': 'A great job opportunity',
            'location': 'Remote',
            'contract_type': 'FULL_TIME',
            'requirements': 'Python, Django',
            'salary': '50000-70000',
            'application_deadline': timezone.now().date() + timezone.timedelta(days=30),
            'number_of_openings': 2,
            'is_remote': True,
            'experience_level': 'MID'
        }

    def test_create_job(self):
        job = Job.objects.create(**self.job_data)
        self.assertEqual(job.title, self.job_data['title'])
        self.assertEqual(job.company, self.company)

    def test_job_str_method(self):
        job = Job.objects.create(**self.job_data)
        expected_str = f"{self.job_data['title']} at {self.company.company_name}"
        self.assertEqual(str(job), expected_str)

    def test_job_is_open(self):
        job = Job.objects.create(**self.job_data)
        self.assertTrue(job.is_open())

        job.status = 'CLOSED'
        job.save()
        self.assertFalse(job.is_open())

        job.status = 'OPEN'
        job.application_deadline = timezone.now().date() - timezone.timedelta(days=1)
        job.save()
        self.assertFalse(job.is_open())

    def test_job_application_count(self):
        job = Job.objects.create(**self.job_data)
        self.assertEqual(job.application_count(), 0)

        # Create some applications
        from apps.applications.models import Application
        Application.objects.create(job=job, user=self.user)
        Application.objects.create(job=job, user=self.user)
        
        self.assertEqual(job.application_count(), 2)

    def test_job_clean_method(self):
        job = Job(**self.job_data)
        job.clean()  # This should not raise any exception

        # Test with past deadline
        job.application_deadline = timezone.now().date() - timezone.timedelta(days=1)
        with self.assertRaises(ValidationError):
            job.clean()