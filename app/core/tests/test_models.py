"""
Test for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
"""
get_user_model makes sure we get whatever user model is
set for the project. So if we overwrite the default user model,
this makes sure we pull our custom one
"""


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email successfully"""
        email = 'test@example.com'
        password = 'testpassword123'
        user = get_user_model().objects.create_user(
            email=email, password=password
        )
        self.assertEqual(user.email, email)
        # check_password checks against hashed value
        self.assertTrue(user.check_password(password))
