from django.db import models
from apps.companies.models import Company

class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    contract_type = models.CharField(max_length=10, choices=[('PERMANENT', 'PERMANENT'), ('TEMPORARY', 'TEMPORARY')])
    requirements = models.TextField()
    salary = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    status = models.CharField(max_length=10, choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED')])

    def __str__(self):
        return f'Job {self.job_id}'
