from django.db import models
from apps.companies.models import Company
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.jobs.constants import CONTRACT_TYPE_CHOICES, EXPERIENCE_LEVEL_CHOICES, STATUS_CHOICES

class Job(models.Model):
    job_id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    company_name = models.CharField(max_length=255, default='Unspecified Company')
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    location = models.CharField(max_length=255, db_index=True)
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPE_CHOICES)
    requirements = models.TextField()
    salary = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN', db_index=True)
    application_deadline = models.DateField()
    number_of_openings = models.PositiveIntegerField(default=1)
    is_remote = models.BooleanField(default=False)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES)
    search_vector = SearchVectorField(null=True, blank=True)
    
    class Meta:
        indexes = [
            GinIndex(fields=['search_vector']),
            models.Index(fields=['created_at', 'status']),
            models.Index(fields=['location', 'contract_type']),
        ]

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"
    
    def clean(self):
        if self.application_deadline and self.application_deadline < timezone.now().date():
            raise ValidationError("Application deadline must be in the future.")

    def is_open(self):
        return (
            self.status == 'OPEN' and 
            self.application_deadline > timezone.now().date()
        )

    def application_count(self):
        return self.applications.count()