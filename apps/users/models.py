from django.db import models
from django.contrib.auth.models import AbstractUser, Group, BaseUserManager, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.users import constants
import uuid

class UserManager(BaseUserManager):
    def create_user(self, username, email_address, password=None, **extra_fields):
        if not email_address:
            raise ValueError('The Email field must be set')
        email_address = self.normalize_email(email_address)
        user = self.model(username=username, email_address=email_address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email_address, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'ADMIN')
        return self.create_user(username, email_address, password, **extra_fields)

class User(AbstractUser):
    user_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    email_address = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, unique=True)
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
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email_address'
    REQUIRED_FIELDS = ['email_address', 'first_name', 'last_name']

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