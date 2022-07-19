"""Views for the recipe APIs"""

from tokenize import Token
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    serializer_class = serializers.RecipeSerializer
    # this specifies what model (objects) to use for the viewset
    queryset = Recipe.objects.all()
    # need to use token auth to access these apis
    authentication_classes = [TokenAuthentication]
    # permission to check for is that they are authenticated
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Override queryset to only pull recipes
        of current user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')
