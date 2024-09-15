from django.db import models
from apps.users.models import User

class Notification(models.Model):
    notification_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[('APPLICATION_UPDATE', 'Application Update'), ('NEW_JOB', 'New Job Match'), ('MESSAGE', 'Message')])

    def __str__(self):
        return f"Notification for {self.user.email}: {self.notification_type}"
