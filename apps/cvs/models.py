import os
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from .constants import CV_FILE_EXTENSIONS, MAX_CV_SIZE

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in CV_FILE_EXTENSIONS:
        raise ValidationError(f'Unsupported file extension. Allowed extensions are {", ".join(CV_FILE_EXTENSIONS)}')

def cv_file_path(instance, filename):
    return f'cvs/user_{instance.user.id}/{filename}'

class CV(models.Model):
    cv_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cvs')
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to=cv_file_path, validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.file_name} - {self.user.email}"

    def clean(self):
        if self.file_path.size > MAX_CV_SIZE:
            raise ValidationError(f"File size must be no more than {MAX_CV_SIZE // (1024 * 1024)} MB.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.is_active:
            CV.objects.filter(user=self.user).update(is_active=False)
        super().save(*args, **kwargs)