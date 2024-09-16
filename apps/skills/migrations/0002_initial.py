# Generated by Django 5.1.1 on 2024-09-16 00:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('skills', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userskill',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='users.user'),
        ),
        migrations.AlterUniqueTogether(
            name='jobskill',
            unique_together={('job', 'skill')},
        ),
        migrations.AlterUniqueTogether(
            name='userskill',
            unique_together={('user', 'skill')},
        ),
    ]