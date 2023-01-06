from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FollowViewSet, IngredientsViewSet,
                    RecipeViewSet, TagViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('users', FollowViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]