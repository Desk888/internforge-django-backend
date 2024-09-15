from django.db import models
from apps.users.models import User

class Cv(models.Model):
    cv_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100)
    file_path = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField()
    is_active = models.BooleanField()

    def __str__(self):
        return f'Cv {self.cv_id}'
