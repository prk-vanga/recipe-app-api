"""Unit tests for user models."""

from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):
    """Class that run unit tests for create user functionality"""

    def test_create_user_with_email_successful(self):
        """
            Unit test method that tests create user functionality,
            It will verify two things
            1. user email address stored in the database properly
            2. pasword stored in database properly

        """

        email = "praveen@exmpale.com"
        password = "testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""

        sample_emails = [
            ['test1@Example.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected_email)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a new user without an
            email address raises ValueError."""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')

    def test_create_superuser(self):
        """Testing that creating super user."""
        user = get_user_model().objects.create_superuser(
            'test1@example.com',
            'sample123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
