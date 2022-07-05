"""
Views for the user API.
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system.
        CreateAPIView class handles creating POST request for you,
        it just needs to know what serializer to use
    """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    # we use our own custom serializer instead of ObtainAuthToken one
    # since we customized it to use email instead of username
    serializer_class = AuthTokenSerializer
    # makes api browserable in UI
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
