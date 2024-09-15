from django.db import models
from apps.users.models import User
from apps.jobs.models import Job
from apps.cvs.models import Cv

class Application(models.Model):
    application_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    cv_id = models.ForeignKey(Cv, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    status = models.CharField(max_length=10, choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED')])
    submitted_at = models.DateTimeField()

    def __str__(self):
        return f'Application {self.application_id}'
