from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status


class CreateUserViewTests(APITestCase):
    """Tests the users create view"""

    def setUp(self) -> None:
        self.url = reverse('user_create')

    def test_create_valid_user_success(self):
        """Test creating user with valid data is successful"""
        data = {
            'email': 'test@email.com',
            'first_name': 'test',
            'last_name': 'test',
            'role': 'Teacher',
            'password': 'test1234',
        }
        res = self.client.post(self.url, data)
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(data['password']))

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        data = {
            'email': 'test@email.com',
            'first_name': 'test',
            'last_name': 'test',
            'role': 'Teacher',
            'password': 'test1234',
        }
        get_user_model().objects.create_user(**data)
        res = self.client.post(self.url, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
