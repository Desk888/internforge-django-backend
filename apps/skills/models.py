from django.db import models
from apps.users.models import User
from apps.jobs.models import Job

class Skill(models.Model):
    skill_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f'Skill {self.skill_id}'

class UserSkill(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.IntegerField()

    def __str__(self):
        return f'UserSkill {self.user_id}'

class JobSkill(models.Model):
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
    is_required = models.BooleanField()

    def __str__(self):
        return f'JobSkill {self.job_id}'