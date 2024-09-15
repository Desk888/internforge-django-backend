from django.db import models
from apps.users.models import User

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField()
    created_at = models.DateTimeField()

    def __str__(self):
        return f'Notification {self.notification_id}'
