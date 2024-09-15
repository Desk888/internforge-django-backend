from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email_address = models.EmailField()
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    address_line_one = models.CharField(max_length=100)
    address_line_two = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    job_title = models.CharField(max_length=100)
    current_company = models.CharField(max_length=100)
    created_at = models.DateTimeField()

    def __str__(self):
        return f'User: {self.first_name} {self.last_name}'