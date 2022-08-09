"""Views for the recipe APIs"""
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    # default serializer to use for all api calls
    serializer_class = serializers.RecipeDetailSerializer
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

    def get_serializer_class(self):
        """Return the serializer class for request.
        This func returns a reference to a class so it can instantiate it."""
        # when list api is called (GET), use a different
        # serializer than default
        if self.action == 'list':
            return serializers.RecipeSerializer
        # everything else use default
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        # When creating a new recipe in this viewset,
        # also call this method to set user as current
        # authenticated user making call. The Serializer
        # we created does not have a user field
        serializer.save(user=self.request.user)


class BaseRecipeAttrViewset(mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes"""
    # Mixins need to come first before genericviewset or it will
    # overwrite funcs needed.
    # In order to be able to be able to update a tag, we just add the
    # updatemodelmixin and it creates everything needed.
    # Same for listing and deleting tags.
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewset):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()

    # Code below is added to base class since its shared with ingredients

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    # def get_queryset(self):
    #     """Filter queryset for authenticated user"""
    #     return self.queryset.filter(user=self.request.user).order_by('-name')


class IngredientViewSet(BaseRecipeAttrViewset):
    """Manage ingredients in the database"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    # def get_queryset(self):
    #     """Filter queryset to authenticated user"""
    #     return self.queryset.filter(user=self.request.user).order_by("-name")
