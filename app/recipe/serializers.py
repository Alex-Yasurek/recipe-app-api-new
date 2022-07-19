"""Serializers for recipe API"""
from rest_framework import serializers
from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""

    class Meta:
        model = Recipe
        # includes all fields from model except description
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view.
    This inherits from recipeSerializer, which inherits
    from ModelSerializer.
    DIfference is this serializer will include descriptions"""

    # inherit from RecipeSerializer.Meta to pull in all the fields
    # listed there
    class Meta(RecipeSerializer.Meta):
        # we want fields inherited plus add description
        fields = RecipeSerializer.Meta.fields + ['description']
