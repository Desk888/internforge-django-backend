from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.notifications.models import Notification
from apps.users.models import User

class NotificationViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.notification_data = {
            'user': self.user,
            'notification_type': 'APPLICATION_STATUS',
            'message': 'Your application status has changed.',
        }

    def test_list_notifications(self):
        Notification.objects.create(**self.notification_data)
        url = reverse('notification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_notification(self):
        notification = Notification.objects.create(**self.notification_data)
        url = reverse('notification-detail', args=[notification.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['notification_type'], 'APPLICATION_STATUS')

    def test_mark_as_read(self):
        notification = Notification.objects.create(**self.notification_data)
        url = reverse('notification-mark-as-read', args=[notification.pk])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_mark_all_as_read(self):
        Notification.objects.create(**self.notification_data)
        Notification.objects.create(**self.notification_data)
        url = reverse('notification-mark-all-as-read')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(n.is_read for n in Notification.objects.all()))

class NotificationServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )

    def test_create_notification(self):
        from apps.notifications.service import NotificationService
        NotificationService.create_notification(
            user=self.user,
            notification_type='TEST_NOTIFICATION',
            message='Test message'
        )
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.notification_type, 'TEST_NOTIFICATION')
        self.assertEqual(notification.message, 'Test message')