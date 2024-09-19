from django.test import TestCase
from apps.notifications.models import Notification
from apps.users.models import User
from django.contrib.contenttypes.models import ContentType

class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.notification_data = {
            'user': self.user,
            'notification_type': 'APPLICATION_STATUS',
            'message': 'Your application status has changed.',
            'related_object_type': 'Application',
            'related_object_id': 1,
        }

    def test_create_notification(self):
        notification = Notification.objects.create(**self.notification_data)
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.notification_type, 'APPLICATION_STATUS')
        self.assertFalse(notification.is_read)

    def test_notification_str_method(self):
        notification = Notification.objects.create(**self.notification_data)
        expected_str = f"Notification for {self.user.email}: APPLICATION_STATUS"
        self.assertEqual(str(notification), expected_str)

    def test_notification_ordering(self):
        Notification.objects.create(**self.notification_data)
        second_notification = Notification.objects.create(
            user=self.user,
            notification_type='NEW_JOB',
            message='A new job has been posted.'
        )
        notifications = Notification.objects.all()
        self.assertEqual(notifications[0], second_notification)

    def test_content_type_assignment(self):
        notification = Notification.objects.create(**self.notification_data)
        self.assertIsNotNone(notification.content_type)
        self.assertEqual(notification.content_type, ContentType.objects.get_for_model(User))