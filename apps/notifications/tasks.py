from project.celery import app
from .models import Notification
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

@app.task
def create_notification(user_id, notification_type, message, related_object_id=None, related_object_type=None):
    logger.info(f"Creating notification: type={notification_type}, user_id={user_id}")
    try:
        with transaction.atomic():
            notification_data = {
                'user_id': user_id,
                'notification_type': notification_type,
                'message': message,
            }
            if related_object_id and related_object_type:
                try:
                    content_type = ContentType.objects.get(model=related_object_type.lower())
                    notification_data.update({
                        'content_type': content_type,
                        'object_id': related_object_id,
                    })
                except ContentType.DoesNotExist:
                    logger.warning(f"ContentType not found for {related_object_type}")
            
            notification = Notification.objects.create(**notification_data)
        logger.info(f"Notification created successfully: id={notification.id}")
    except Exception as e:
        logger.error(f"Failed to create notification: {str(e)}", exc_info=True)
        raise

@app.task
def notify_application_status_change(application_id):
    logger.info(f"Notifying application status change: application_id={application_id}")
    try:
        from apps.applications.models import Application
        with transaction.atomic():
            application = Application.objects.select_related('job', 'user').get(id=application_id)
            message = f"The status of your application for {application.job.title} has changed to {application.get_status_display()}."
            create_notification.delay(
                user_id=application.user.id,
                notification_type='APPLICATION_STATUS',
                message=message,
                related_object_id=application.id,
                related_object_type='Application'
            )
        logger.info(f"Application status change notification queued: application_id={application_id}")
    except Application.DoesNotExist:
        logger.error(f"Application not found: id={application_id}")
    except Exception as e:
        logger.error(f"Failed to notify application status change: {str(e)}", exc_info=True)
        raise

@app.task
def notify_new_job_posted(job_id):
    logger.info(f"Notifying new job posted: job_id={job_id}")
    try:
        from apps.jobs.models import Job
        from apps.companies.models import Company
        with transaction.atomic():
            job = Job.objects.select_related('company').get(id=job_id)
            company = job.company
            followers = company.followers.all() if hasattr(company, 'followers') else []
            for user in followers:
                message = f"A new job '{job.title}' has been posted by {company.name}."
                create_notification.delay(
                    user_id=user.id,
                    notification_type='NEW_JOB',
                    message=message,
                    related_object_id=job.id,
                    related_object_type='Job'
                )
        logger.info(f"New job notifications queued: job_id={job_id}, follower_count={len(followers)}")
    except Job.DoesNotExist:
        logger.error(f"Job not found: id={job_id}")
    except Exception as e:
        logger.error(f"Failed to notify new job posted: {str(e)}", exc_info=True)
        raise

@app.task
def notify_application_received(application_id):
    logger.info(f"Notifying application received: application_id={application_id}")
    try:
        from apps.applications.models import Application
        with transaction.atomic():
            application = Application.objects.select_related('job', 'user', 'job__company').get(id=application_id)
            message = f"You have received a new application for the job '{application.job.title}' from {application.user.get_full_name()}."
            create_notification.delay(
                user_id=application.job.company.user.id,
                notification_type='APPLICATION_RECEIVED',
                message=message,
                related_object_id=application.id,
                related_object_type='Application'
            )
        logger.info(f"Application received notification queued: application_id={application_id}")
    except Application.DoesNotExist:
        logger.error(f"Application not found: id={application_id}")
    except Exception as e:
        logger.error(f"Failed to notify application received: {str(e)}", exc_info=True)
        raise

@app.task
def clean_old_notifications():
    logger.info("Starting cleanup of old notifications")
    try:
        from django.utils import timezone
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        deleted_count, _ = Notification.objects.filter(created_at__lt=thirty_days_ago, is_read=True).delete()
        logger.info(f"Cleaned up {deleted_count} old notifications")
    except Exception as e:
        logger.error(f"Failed to clean up old notifications: {str(e)}", exc_info=True)
        raise