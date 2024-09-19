from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from apps.cvs.models import CV
from apps.users.models import User
import os

class CVModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.cv_data = {
            'user': self.user,
            'file_name': 'test_cv.pdf',
            'file_path': SimpleUploadedFile("test_cv.pdf", b"file_content", content_type="application/pdf")
        }

    def test_create_cv(self):
        cv = CV.objects.create(**self.cv_data)
        self.assertEqual(cv.user, self.user)
        self.assertEqual(cv.file_name, 'test_cv.pdf')
        self.assertTrue(cv.is_active)

    def test_cv_str_method(self):
        cv = CV.objects.create(**self.cv_data)
        expected_str = f"test_cv.pdf - {self.user.email}"
        self.assertEqual(str(cv), expected_str)

    def test_cv_file_extension_validation(self):
        invalid_cv_data = self.cv_data.copy()
        invalid_cv_data['file_path'] = SimpleUploadedFile("test_cv.txt", b"file_content", content_type="text/plain")
        with self.assertRaises(ValidationError):
            CV.objects.create(**invalid_cv_data)

    def test_cv_file_size_validation(self):
        large_file_content = b"x" * (5 * 1024 * 1024 + 1)  # 5MB + 1 byte
        invalid_cv_data = self.cv_data.copy()
        invalid_cv_data['file_path'] = SimpleUploadedFile("large_cv.pdf", large_file_content, content_type="application/pdf")
        with self.assertRaises(ValidationError):
            CV.objects.create(**invalid_cv_data)

    def test_cv_active_status(self):
        cv1 = CV.objects.create(**self.cv_data)
        cv2 = CV.objects.create(user=self.user, file_name='test_cv2.pdf', file_path=SimpleUploadedFile("test_cv2.pdf", b"file_content", content_type="application/pdf"))
        
        cv1.refresh_from_db()
        cv2.refresh_from_db()

        self.assertFalse(cv1.is_active)
        self.assertTrue(cv2.is_active)

    def tearDown(self):
        for cv in CV.objects.all():
            if os.path.isfile(cv.file_path.path):
                os.remove(cv.file_path.path)