"""
Database models.
admin login info: admin@exmaple.com/password1
"""
from django.conf import settings
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

        # dont create user if no email is provided
        if not email:
            raise ValueError('User must have an email address')

        # self.model refers to User model since its a UserManager
        # normalize_email is part of baseUserManager class
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # set_password will encrypt password
        user.set_password(password)
        # dont need to but passing in using=self._db future proofs
        # this in case we ever add multiple DBs
        user.save(using=self._db)
        return user

    # overwrite create_superuser func from BaseUserManager
    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        # call default create_user method
        user = self.create_user(email, password)
        # is_staff has to be true to login into admin area
        user.is_staff = True
        user.is_superuser = True
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


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')

    # Decides what will be displayed in django admin
    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
