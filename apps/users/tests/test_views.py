from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

User = get_user_model()

class UserViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email_address': 'testuser@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'JOB_SEEKER'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'email_address': 'newuser@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'user_type': 'JOB_SEEKER'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_retrieve_user(self):
        url = reverse('user-detail', args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email_address'], self.user.email_address)

    def test_update_user(self):
        url = reverse('user-detail', args=[self.user.pk])
        data = {'first_name': 'Updated'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_delete_user(self):
        url = reverse('user-detail', args=[self.user.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

class UserCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        url = reverse('user-register')
        data = {
            'username': 'newuser',
            'email_address': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_registration_password_mismatch(self):
        url = reverse('user-register')
        data = {
            'username': 'newuser',
            'email_address': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'differentpass',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class VerifyEmailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email_address='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.user.email_verification_token = 'test-token'
        self.user.save()

    def test_verify_email(self):
        url = reverse('verify-email', args=['test-token'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.email_verified)

    def test_verify_email_invalid_token(self):
        url = reverse('verify-email', args=['invalid-token'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class PasswordResetViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email_address='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_password_reset_request(self):
        url = reverse('password-reset')
        data = {'email_address': 'testuser@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Password reset email has been sent.")

    def test_password_reset_invalid_email(self):
        url = reverse('password-reset')
        data = {'email_address': 'nonexistent@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class SetNewPasswordViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email_address='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = PasswordResetTokenGenerator().make_token(self.user)

    def test_set_new_password(self):
        url = reverse('set-new-password')
        data = {
            'password': 'newtestpass123',
            'token': self.token,
            'uidb64': self.uid
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newtestpass123'))

    def test_set_new_password_invalid_token(self):
        url = reverse('set-new-password')
        data = {
            'password': 'newtestpass123',
            'token': 'invalid-token',
            'uidb64': self.uid
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)