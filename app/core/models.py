"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users"""

    # overwrite create_user func from BaseUserManager class
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        # self.model refers to User model since its a UserManager
        user = self.model(email=email, **extra_fields)
        # set_password will encrypt password
        user.set_password(password)
        # dont need to but passing in using=self._db future proofs
        # this in case we ever add multiple DBs
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Will overwrite default django user model with our own
    custom model that uses email instead of username.
    PermissionsMixin handles adding permissions to users
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # assign user model to User manager
    objects = UserManager()

    # field we want to use for authentication
    USERNAME_FIELD = 'email'
