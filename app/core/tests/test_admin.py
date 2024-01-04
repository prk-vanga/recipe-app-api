"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTest(TestCase):
    """Tests for django admin."""

    def setUp(self):
        """
        Create User and Client.
        These are the modules setup in this method
        which will be used by each/every single test defined in this class
        """

        self.client = Client() # this is test client, which will allow us to make http requests # noqa
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='sample123',
        )
        # Every request we make through this client is going to be authenticated with this user # noqa
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User',
        )

    def test_users_list(self):
        """Tests our users are listed in the page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_update_users(self):
        """Test functionality of deleting/updating users in Admin site."""

        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_add_users(self):
        """Testing functionality of creating users in Admin page."""

        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
