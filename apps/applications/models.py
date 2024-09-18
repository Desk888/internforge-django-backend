from django.db import models
from apps.users.models import User
from apps.jobs.models import Job
from apps.cvs.models import CV
from apps.applications.constants import APPLICATION_STATUS

class Application(models.Model):
    application_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    cv = models.ForeignKey(CV, on_delete=models.SET_NULL, null=True, related_name='applications')
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='PENDING')
    submitted_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    interviewer_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.email}'s application for {self.job.title}"
    
    class Meta:
        ordering = ['-submitted_at']
        unique_together = ('user', 'job')