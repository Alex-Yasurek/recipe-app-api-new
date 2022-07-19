"""
Django admin customization
"""
from django.contrib import admin
# we call our model UserAdmin so we rename this import so they dont collide
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# this helps with translation of text
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    # -----------Viewing all users
    # how to order users on admin user list page
    ordering = ['id']
    # what fields to display in list
    list_display = ['email', 'name']

    # -------------Viewing User
    # create grouping of fields to show when viewing
    # individual user accounts.
    # name of grouping to display, {fields: to show}
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',)}),
        (_('Important Dates'), {'fields': ('last_login',)}),
    )
    # which fields to mark as read only
    readonly_fields = ['last_login']

    # ---------Creating users
    # fields to display when creating a new user in the admin section
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': (
            'email',
            'password1',
            'password2',
            'name',
            'is_active',
            'is_staff',
            'is_superuser',
        )}),
    )


# register User model to display in admin and use
# our custom UserAdmin class to define what should be displayed
# since we changed the default user class
# If not it will try to use the defualt UserAdmin class and throw errors
# since we changed it
admin.site.register(models.User, UserAdmin)
# When registering regular classes you just need to add the class
admin.site.register(models.Recipe)
