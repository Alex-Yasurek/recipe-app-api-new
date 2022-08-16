"""Views for the recipe APIs"""
from drf_spectacular.utils import (
    extend_schema_view, extend_schema,
    OpenApiParameter, OpenApiTypes,
)
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Recipe, Tag, Ingredient
from recipe import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of IDs to filter',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredient IDs to filter',
            )
        ]
    )
)
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

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Override queryset to only pull recipes
        of current user and filter results if passed in"""
        # return self.queryset.filter(user=self.request.user).order_by('-id')
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tags_id = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tags_id)
        if ingredients:
            ingredients_id = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredients_id)

        return queryset.filter(user=self.request.user
                               ).order_by('-id').distinct()

    def get_serializer_class(self):
        """Return the serializer class for request.
        This func returns a reference to a class so it can instantiate it."""
        # when list api is called (GET), use a different
        # serializer than default, same for image uploading
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        # everything else use default
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        # When creating a new recipe in this viewset,
        # also call this method to set user as current
        # authenticated user making call. The Serializer
        # we created does not have a user field
        serializer.save(user=self.request.user)

    # custom action: only accepts POST, only
    # applies to detail portion of model viewset, path for custom action
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe"""
        # get recipe of PK supplied
        recipe = self.get_object()
        # call get_serializer func to get serializer,
        # since it returns a function we pass params
        # as if we are calling it
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description="Filter by items assigned to recipe.",
            )
        ]
    )
)
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
        # will convert 1 or 0 into true/false
        # return self.queryset.filter(user=self.request.user).order_by('-name')
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(user=self.request.user
                               ).order_by('-name').distinct()


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
