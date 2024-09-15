from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.users.models import User
from apps.jobs.models import Job

class Skill(models.Model):
    skill_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=[('TECHNICAL', 'Technical'), ('SOFT', 'Soft Skill'), ('LANGUAGE', 'Language')])

    def __str__(self):
        return self.name

class UserSkill(models.Model):
    user_skill_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    acquired = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user.email}'s {self.skill.name} skill"

class JobSkill(models.Model):
    job_skill_id = models.BigAutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='required_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    is_required = models.BooleanField(default=True)
    importance_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ('job', 'skill')

    def __str__(self):
        return f"{self.skill.name} for {self.job.title}"