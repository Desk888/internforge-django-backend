from django.db import models
from apps.users.models import User

class CV(models.Model):
    cv_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cvs')
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='cvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    version = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.email}'s CV - {self.file_name}"