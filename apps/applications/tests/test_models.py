from django.test import TestCase
from apps.applications.models import Application
from apps.users.models import User
from apps.companies.models import Company
from apps.jobs.models import Job
from apps.cvs.models import CV
from django.utils import timezone

class ApplicationModelTest(TestCase):
    def setUp(self):
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
        self.application_data = {
            'user': self.user,
            'job': self.job,
            'cv': self.cv,
            'cover_letter': 'I am very interested in this position.',
            'status': 'PENDING'
        }

    def test_create_application(self):
        application = Application.objects.create(**self.application_data)
        self.assertEqual(application.user, self.user)
        self.assertEqual(application.job, self.job)
        self.assertEqual(application.status, 'PENDING')

    def test_application_str_method(self):
        application = Application.objects.create(**self.application_data)
        expected_str = f"{self.user.email}'s application for {self.job.title}"
        self.assertEqual(str(application), expected_str)

    def test_application_unique_constraint(self):
        Application.objects.create(**self.application_data)
        with self.assertRaises(Exception):  # This should raise an IntegrityError
            Application.objects.create(**self.application_data)

    def test_application_status_change(self):
        application = Application.objects.create(**self.application_data)
        self.assertEqual(application.status, 'PENDING')

        application.status = 'REVIEWED'
        application.save()
        self.assertEqual(application.status, 'REVIEWED')

    def test_application_ordering(self):
        Application.objects.create(**self.application_data)
        second_application = Application.objects.create(
            user=self.user,
            job=Job.objects.create(company=self.company, title='Another Job'),
            cv=self.cv,
            cover_letter='Another application'
        )
        applications = Application.objects.all()
        self.assertEqual(applications[0], second_application)  # The latest application should be first