from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase


class UserModelTests(APITestCase):
    def test_create_user_successful(self):
        """Test creating a new user"""
        email = 'test@email.com'
        password = 'test1234'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')

    def test_new_user_invalid_password(self):
        """Test creating user with no password raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('test@email.com', None)

    def test_create_new_superuser(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser('test@email.com', 'test1234')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
