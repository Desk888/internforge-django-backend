# apps/notifications/tasks.py

from project.celery import app
from .models import Notification

@app.task
def create_notification(user_id, notification_type, message, related_object_id=None, related_object_type=None):
    Notification.objects.create(
        user_id=user_id,
        notification_type=notification_type,
        message=message,
        related_object_id=related_object_id,
        related_object_type=related_object_type
    )

@app.task
def notify_application_status_change(application_id):
    from apps.applications.models import Application
    application = Application.objects.get(id=application_id)
    message = f"The status of your application for {application.job.title} has changed to {application.get_status_display()}."
    create_notification.delay(
        user_id=application.user.id,
        notification_type='APPLICATION_STATUS',
        message=message,
        related_object_id=application.id,
        related_object_type='Application'
    )

@app.task
def notify_new_job_posted(job_id):
    from apps.jobs.models import Job
    job = Job.objects.get(id=job_id)
    for user in job.company.followers.all():
        message = f"A new job '{job.title}' has been posted by {job.company.name}."
        create_notification.delay(
            user_id=user.id,
            notification_type='NEW_JOB',
            message=message,
            related_object_id=job.id,
            related_object_type='Job'
        )

@app.task
def notify_application_received(application_id):
    from apps.applications.models import Application
    application = Application.objects.get(id=application_id)
    message = f"You have received a new application for the job '{application.job.title}' from {application.user.get_full_name()}."
    create_notification.delay(
        user_id=application.job.company.user.id,
        notification_type='APPLICATION_RECEIVED',
        message=message,
        related_object_id=application.id,
        related_object_type='Application'
    )
