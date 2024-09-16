# Generated by Django 5.1.1 on 2024-09-16 00:22

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('skill_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(choices=[('TECHNICAL', 'Technical'), ('SOFT', 'Soft Skill'), ('LANGUAGE', 'Language')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='JobSkill',
            fields=[
                ('job_skill_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('is_required', models.BooleanField(default=True)),
                ('importance_level', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='required_skills', to='jobs.job')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skills.skill')),
            ],
        ),
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('user_skill_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('proficiency_level', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('acquired', models.DateField(blank=True, null=True)),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skills.skill')),
            ],
        ),
    ]