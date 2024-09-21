from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email_address': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'JOB_SEEKER'
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email_address, self.user_data['email_address'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.user_type, self.user_data['user_type'])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username='admin',
            email_address='admin@example.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.user_type, 'ADMIN')

    def test_user_str_method(self):
        user = User.objects.create_user(**self.user_data)
        expected_str = f"{self.user_data['first_name']} {self.user_data['last_name']} ({self.user_data['email_address']})"
        self.assertEqual(str(user), expected_str)

    def test_user_email_uniqueness(self):
        User.objects.create_user(**self.user_data)
        duplicate_user_data = self.user_data.copy()
        duplicate_user_data['username'] = 'testuser2'
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**duplicate_user_data)

    def test_user_username_uniqueness(self):
        User.objects.create_user(**self.user_data)
        duplicate_user_data = self.user_data.copy()
        duplicate_user_data['email_address'] = 'test2@example.com'
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**duplicate_user_data)

    def test_user_group_assignment(self):
        user = User.objects.create_user(**self.user_data)
        self.assertTrue(user.groups.filter(name='JOB_SEEKER').exists())

        employer_data = self.user_data.copy()
        employer_data['username'] = 'employer'
        employer_data['email_address'] = 'employer@example.com'
        employer_data['user_type'] = 'EMPLOYER'
        employer = User.objects.create_user(**employer_data)
        self.assertTrue(employer.groups.filter(name='EMPLOYER').exists())

    def test_default_user_type(self):
        user_data = self.user_data.copy()
        del user_data['user_type']
        user = User.objects.create_user(**user_data)
        self.assertEqual(user.user_type, 'SEEKER')

    def test_email_verification_token(self):
        user = User.objects.create_user(**self.user_data)
        self.assertIsNotNone(user.email_verification_token)
        self.assertFalse(user.email_verified)

    def test_create_user_without_username(self):
        user_data = self.user_data.copy()
        del user_data['username']
        with self.assertRaises(TypeError):
            User.objects.create_user(**user_data)

    def test_create_user_without_email(self):
        user_data = self.user_data.copy()
        del user_data['email_address']
        with self.assertRaises(ValueError):
            User.objects.create_user(**user_data)

    def test_create_superuser_with_is_staff_false(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='admin',
                email_address='admin@example.com',
                password='adminpass123',
                is_staff=False
            )

    def test_create_superuser_with_is_superuser_false(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='admin',
                email_address='admin@example.com',
                password='adminpass123',
                is_superuser=False
            )