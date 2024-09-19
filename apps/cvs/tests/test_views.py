from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.cvs.models import CV
from apps.users.models import User
import os

class CVViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client.force_authenticate(user=self.user)
        self.cv_data = {
            'file_name': 'test_cv.pdf',
            'file_path': SimpleUploadedFile("test_cv.pdf", b"file_content", content_type="application/pdf")
        }

    def test_upload_cv(self):
        url = reverse('cv-list')
        response = self.client.post(url, self.cv_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CV.objects.count(), 1)
        self.assertEqual(CV.objects.get().user, self.user)

    def test_retrieve_cv(self):
        cv = CV.objects.create(user=self.user, **self.cv_data)
        url = reverse('cv-detail', args=[cv.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file_name'], 'test_cv.pdf')

    def test_update_cv(self):
        cv = CV.objects.create(user=self.user, **self.cv_data)
        url = reverse('cv-detail', args=[cv.pk])
        updated_data = {
            'file_name': 'updated_cv.pdf',
            'file_path': SimpleUploadedFile("updated_cv.pdf", b"updated_content", content_type="application/pdf")
        }
        response = self.client.put(url, updated_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cv.refresh_from_db()
        self.assertEqual(cv.file_name, 'updated_cv.pdf')

    def test_delete_cv(self):
        cv = CV.objects.create(user=self.user, **self.cv_data)
        url = reverse('cv-detail', args=[cv.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CV.objects.count(), 0)

    def test_list_cvs(self):
        CV.objects.create(user=self.user, **self.cv_data)
        url = reverse('cv-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_set_active_cv(self):
        cv1 = CV.objects.create(user=self.user, **self.cv_data)
        cv2 = CV.objects.create(user=self.user, file_name='test_cv2.pdf', file_path=SimpleUploadedFile("test_cv2.pdf", b"file_content", content_type="application/pdf"))
        
        url = reverse('cv-set-active', args=[cv1.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        cv1.refresh_from_db()
        cv2.refresh_from_db()
        self.assertTrue(cv1.is_active)
        self.assertFalse(cv2.is_active)

    def test_delete_active_cv(self):
        cv = CV.objects.create(user=self.user, **self.cv_data)
        url = reverse('cv-detail', args=[cv.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CV.objects.count(), 1)

    def tearDown(self):
        for cv in CV.objects.all():
            if os.path.isfile(cv.file_path.path):
                os.remove(cv.file_path.path)