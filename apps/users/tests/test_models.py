from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'JOB_SEEKER'
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.user_type, self.user_data['user_type'])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_str_method(self):
        user = User.objects.create_user(**self.user_data)
        expected_str = f"{self.user_data['first_name']} {self.user_data['last_name']} ({self.user_data['email']})"
        self.assertEqual(str(user), expected_str)

    def test_user_clean_method(self):
        user = User(**self.user_data)
        user.clean()  # This should not raise any exception

        # Test with invalid email
        user.email = 'invalid_email'
        with self.assertRaises(ValidationError):
            user.clean()

    def test_user_group_assignment(self):
        user = User.objects.create_user(**self.user_data)
        self.assertTrue(user.groups.filter(name='JOB_SEEKER').exists())

        employer_data = self.user_data.copy()
        employer_data['email'] = 'employer@example.com'
        employer_data['user_type'] = 'EMPLOYER'
        employer = User.objects.create_user(**employer_data)
        self.assertTrue(employer.groups.filter(name='EMPLOYER').exists())