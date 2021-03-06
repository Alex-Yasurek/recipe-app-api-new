"""
Test for models.
"""
from decimal import Decimal
from django.test import TestCase
# used to test the user model since we overwrite a default model
from django.contrib.auth import get_user_model

# need to import models when testing other non-user models
from core import models
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

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a super user"""
        user = get_user_model().objects.create_superuser(
            'test@example.com', 'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successful"""
        user = get_user_model().objects.create_user(
            'test@example.com', 'testpass123'
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description',
        )
        self.assertEqual(str(recipe), recipe.title)
