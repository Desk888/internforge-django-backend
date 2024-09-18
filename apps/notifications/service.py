from .tasks import (create_notification, notify_application_status_change, 
                    notify_new_job_posted, notify_application_received)
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    def create_notification(user, notification_type, message, related_object=None):
        try:
            create_notification.delay(
                user_id=user.id,
                notification_type=notification_type,
                message=message,
                related_object_id=related_object.id if related_object else None,
                related_object_type=related_object._meta.model_name if related_object else None
            )
        except Exception as e:
            logger.error(f"Failed to create notification: {str(e)}")

    @staticmethod
    def notify_application_status_change(application):
        notify_application_status_change.delay(application.id)

    @staticmethod
    def notify_new_job_posted(job):
        notify_new_job_posted.delay(job.id)

    @staticmethod
    def notify_application_received(application):
        notify_application_received.delay(application.id)