from django.db import models
from apps.users.models import User
from apps.jobs.models import Job
from apps.cvs.models import CV

class Application(models.Model):
    application_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    cv = models.ForeignKey(CV, on_delete=models.SET_NULL, null=True, related_name='applications')
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=[('SUBMITTED', 'Submitted'), ('UNDER_REVIEW', 'Under Review'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='SUBMITTED')
    submitted_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    interviewer_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.email}'s application for {self.job.title}"
