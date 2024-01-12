"""
Test for user API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Creates and returns new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    """Test public feature of API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successfull."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test User 1',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_returns_error(self):
        """Test if created user already present return Error message."""
        payload = {
            'email': 'testuser1@example.com',
            'password': 'testpass123',
            'name': 'Test User 1'
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_too_short_password(self):
        """Test verification of password length."""
        payload = {
            'email': 'testuser1@exmple.com',
            'password': 'pw1',
            'name': 'Test User 1'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()

        self.assertFalse(user_exists)
