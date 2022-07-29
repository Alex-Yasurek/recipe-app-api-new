"""Serializers for recipe API"""
from rest_framework import serializers
from core.models import Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        # includes all fields from model except description
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a recipe"""
        # remove tags from data
        tags = validated_data.pop('tags', [])
        # create recipe without tags data since tags have
        # to be added afterwards
        recipe = Recipe.objects.create(**validated_data)
        # get user who made call
        auth_user = self.context['request'].user

        for tag in tags:
            # create or retrieve tag if already exists
            tags_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                # **tag future proofs it incase we add new things tags
                **tag
            )
            # add tag to recipe
            recipe.tags.add(tags_obj)

        return recipe


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
