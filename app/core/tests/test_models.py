from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@testdomain.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """ Test creating a new user with email is successful."""
        email = "test@testdomain.com"
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
            )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Test the email for a new user is normalized."""
        email = "test@TESTDOMAIN.COM"
        user = get_user_model().objects.create_user(email, "test123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")

    def test_create_new_superuser(self):
        """ Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            "test@test.com",
            "test123"
            )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_label_str(self):
        """ Test the label string representation"""
        label = models.Label.objects.create(
            user=sample_user(),
            name='Diabetes'
        )

        self.assertEqual(str(label), label.name)

    def test_patient_info_str(self):
        """ Test the patient info string representation"""
        patient_info = models.PatientInfo.objects.create(
            user=sample_user(),
            name='Test patient'
        )

        self.assertEqual(str(patient_info), patient_info.name)

    def test_image_str(self):
        """Test the image string representation."""
        image = models.Image.objects.create(
            user=sample_user(),
            title="Dear patient1 MRI Image",
            date="2020-05-12",
            status="New status",
        )
        self.assertEqual(str(image), image.title)

    @patch('uuid.uuid4')
    def test_image_file_name_uuid(self, mock_uuid):
        """ Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/image/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
