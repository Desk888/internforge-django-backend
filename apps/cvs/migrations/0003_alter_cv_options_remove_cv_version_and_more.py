# Generated by Django 5.1.1 on 2024-09-18 12:24

import apps.cvs.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvs', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cv',
            options={'ordering': ['-uploaded_at']},
        ),
        migrations.RemoveField(
            model_name='cv',
            name='version',
        ),
        migrations.AlterField(
            model_name='cv',
            name='file_path',
            field=models.FileField(upload_to=apps.cvs.models.cv_file_path, validators=[apps.cvs.models.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='cv',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cvs', to=settings.AUTH_USER_MODEL),
        ),
    ]
