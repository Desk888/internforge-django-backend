from django.db import models
from apps.users.models import User

class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField()
    address_line_one = models.CharField(max_length=100)
    address_line_two = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    industry = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Company {self.company_id}'