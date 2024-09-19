from django.test import TestCase
from apps.skills.models import Skill, UserSkill, JobSkill
from apps.users.models import User
from apps.jobs.models import Job
from apps.companies.models import Company

class SkillModelTest(TestCase):
    def setUp(self):
        self.skill_data = {
            'name': 'Python',
            'description': 'Programming language',
            'category': 'TECHNICAL'
        }

    def test_create_skill(self):
        skill = Skill.objects.create(**self.skill_data)
        self.assertEqual(skill.name, 'Python')
        self.assertEqual(skill.category, 'TECHNICAL')

    def test_skill_str_method(self):
        skill = Skill.objects.create(**self.skill_data)
        self.assertEqual(str(skill), 'Python')

class UserSkillModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.skill = Skill.objects.create(name='Python', category='TECHNICAL')
        self.user_skill_data = {
            'user': self.user,
            'skill': self.skill,
            'proficiency_level': 4
        }

    def test_create_user_skill(self):
        user_skill = UserSkill.objects.create(**self.user_skill_data)
        self.assertEqual(user_skill.user, self.user)
        self.assertEqual(user_skill.skill, self.skill)
        self.assertEqual(user_skill.proficiency_level, 4)

    def test_user_skill_str_method(self):
        user_skill = UserSkill.objects.create(**self.user_skill_data)
        expected_str = f"{self.user.email}'s Python skill"
        self.assertEqual(str(user_skill), expected_str)

class JobSkillModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(company_name='Test Company')
        self.job = Job.objects.create(
            company=self.company,
            title='Software Developer'
        )
        self.skill = Skill.objects.create(name='Python', category='TECHNICAL')
        self.job_skill_data = {
            'job': self.job,
            'skill': self.skill,
            'importance_level': 5
        }

    def test_create_job_skill(self):
        job_skill = JobSkill.objects.create(**self.job_skill_data)
        self.assertEqual(job_skill.job, self.job)
        self.assertEqual(job_skill.skill, self.skill)
        self.assertEqual(job_skill.importance_level, 5)

    def test_job_skill_str_method(self):
        job_skill = JobSkill.objects.create(**self.job_skill_data)
        expected_str = f"Python for Software Developer"
        self.assertEqual(str(job_skill), expected_str)