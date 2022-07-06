"""Serializers for the user API View."""
from django.contrib.auth import (get_user_model, authenticate)
from rest_framework import serializers
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    """
        Serialzier for the user object.
        Converts to and from python objects.
        Takes json input from an API, validates it, converts
        it into python object
    """

    class Meta:
        # lets serializer know what model it is representing
        model = get_user_model()

        # fields we want to make available through serializer.
        # Min fields required to create a user. We dont want users to
        # be able to set is_staff or is_active.
        # These are the fields they can update through api.
        fields = ['email', 'password', 'name']
        # user can set password but not get it returned
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password
            Will only be called is data was validated
            (eg: password min length >=5)
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Overwrite update method on user serializer"""
        # remove password from dictionary
        password = validated_data.pop('password', None)
        # call update method on model serializer base class
        user = super().update(instance, validated_data)
        # only update password if user sent one, if not leave original
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the use auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenicate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        # authenticate() comes built in and requires 3 params
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            # this error will be translated into a 400 error
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
