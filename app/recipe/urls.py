"""URL mappings for recipe app"""
from django.urls import (path, include)
from rest_framework.routers import DefaultRouter
from recipe import views

# used to automatically create routes for all the options
# available for the view. Since we are using the
# ModelViewset then it will create endpoints for CRUD
# create urls for: GET, POST, PUT, PATCH, DELETE
router = DefaultRouter()
# register viewset and give it name
# apis will be /api/recipes/...
router.register('recipes', views.RecipeViewSet)

# this will be used for reverse look up of urls
app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
