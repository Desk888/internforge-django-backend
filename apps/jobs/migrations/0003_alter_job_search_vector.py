# Generated by Django 5.1.1 on 2024-09-16 23:52

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_job_search_vector_job_jobs_job_search__684d46_gin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(blank=True, null=True),
        ),
    ]