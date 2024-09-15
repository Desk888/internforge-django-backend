from django.db import models
from apps.users.models import User

class Company(models.Model):
    company_id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField()
    address_line_one = models.CharField(max_length=255)
    address_line_two = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    industry = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_companies')
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    employee_count = models.PositiveIntegerField(null=True, blank=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    company_status = models.CharField(max_length=20, choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('VERIFIED', 'Verified')], default='ACTIVE')

    def __str__(self):
        return self.company_name