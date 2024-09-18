from django.db import models
from .constants import NOTIFICATION_TYPES
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.apps import apps

def get_default_content_type():
    User = apps.get_model(settings.AUTH_USER_MODEL)
    return ContentType.objects.get_for_model(User).id

class Notification(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE, 
        related_name='notifications', 
        default=get_default_content_type
    )
    
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.email}: {self.notification_type}"

    def save(self, *args, **kwargs):
        if self.object_id and not self.content_type:
            self.content_type = ContentType.objects.get_for_model(settings.AUTH_USER_MODEL)
        super().save(*args, **kwargs)