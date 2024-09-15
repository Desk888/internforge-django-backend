from django.db import models
from apps.companies.models import Company

class Job(models.Model):
    job_id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    contract_type = models.CharField(max_length=20, choices=[('FULL_TIME', 'Full Time'), ('PART_TIME', 'Part Time'), ('CONTRACT', 'Contract'), ('INTERNSHIP', 'Internship')])
    requirements = models.TextField()
    salary = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('OPEN', 'Open'), ('CLOSED', 'Closed'), ('DRAFT', 'Draft')], default='OPEN')
    application_deadline = models.DateField()
    number_of_openings = models.PositiveIntegerField(default=1)
    is_remote = models.BooleanField(default=False)
    experience_level = models.CharField(max_length=20, choices=[('ENTRY', 'Entry Level'), ('MID', 'Mid Level'), ('SENIOR', 'Senior Level')])

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"