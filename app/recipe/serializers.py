"""Serializers for recipe API"""
from rest_framework import serializers
from core.models import Recipe, Tag, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingedients"""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


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

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed"""
        # get user who made call
        auth_user = self.context['request'].user
        for tag in tags:
            # create or retrieve tag if already exists
            tags_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                # **tag future proofs it incase we add new things to tags
                **tag
            )
            # add tag to recipe
            recipe.tags.add(tags_obj)

    def create(self, validated_data):
        """Create a recipe"""
        # remove tags from data
        tags = validated_data.pop('tags', [])
        # create recipe without tags data since tags have
        # to be added afterwards
        recipe = Recipe.objects.create(**validated_data)

        self._get_or_create_tags(tags, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update recipe"""
        # instance=existing instance we are updating
        tags = validated_data.pop('tags', None)
        # if an empty list or tags were passed, then assign it to instance
        # empty list will mean to just remove all tags
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        # this will reassign rest of attributes to instance
        # since we only cared about tags
        for attr, val in validated_data.items():
            setattr(instance, attr, val)

        instance.save()
        return instance


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
