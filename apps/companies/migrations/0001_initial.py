# Generated by Django 5.1.1 on 2024-09-16 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('website', models.URLField()),
                ('address_line_one', models.CharField(max_length=255)),
                ('address_line_two', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=20)),
                ('industry', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company_logos/')),
                ('employee_count', models.PositiveIntegerField(blank=True, null=True)),
                ('founded_year', models.PositiveIntegerField(blank=True, null=True)),
                ('company_status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('VERIFIED', 'Verified')], default='ACTIVE', max_length=20)),
            ],
        ),
    ]
