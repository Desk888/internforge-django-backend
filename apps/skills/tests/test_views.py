from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.skills.models import Skill
from apps.users.models import User

class SkillViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.skill_data = {
            'name': 'Python',
            'description': 'Programming language',
            'category': 'TECHNICAL'
        }

    def test_create_skill(self):
        url = reverse('skill-list')
        response = self.client.post(url, self.skill_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Skill.objects.count(), 1)
        self.assertEqual(Skill.objects.get().name, 'Python')

    def test_retrieve_skill(self):
        skill = Skill.objects.create(**self.skill_data)
        url = reverse('skill-detail', args=[skill.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Python')

    def test_update_skill(self):
        skill = Skill.objects.create(**self.skill_data)
        url = reverse('skill-detail', args=[skill.pk])
        updated_data = {'name': 'Python 3'}
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Skill.objects.get().name, 'Python 3')

    def test_delete_skill(self):
        skill = Skill.objects.create(**self.skill_data)
        url = reverse('skill-detail', args=[skill.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Skill.objects.count(), 0)

    def test_list_skills(self):
        Skill.objects.create(**self.skill_data)
        url = reverse('skill-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)