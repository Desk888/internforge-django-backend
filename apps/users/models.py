from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    user_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    email_address = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address_line_one = models.CharField(max_length=255, blank=True)
    address_line_two = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    current_company = models.CharField(max_length=100, blank=True)
    user_type = models.CharField(max_length=20, choices=[('SEEKER', 'Job Seeker'), ('EMPLOYER', 'Employer'), ('ADMIN', 'Admin')], default='SEEKER')
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email_address})"