from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.users import constants
import uuid

class User(AbstractUser):
    user_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    email_address = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=20, blank=True)
    address_line_one = models.CharField(max_length=255, blank=True)
    address_line_two = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    current_company = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=20, choices=constants.USER_TYPE_CHOICES, default='SEEKER')
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)
        if creating:
            group, created = Group.objects.get_or_create(name=self.user_type)
            self.groups.add(group)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email_address})"
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user',
    )