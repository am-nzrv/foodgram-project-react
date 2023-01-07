from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FollowViewSet, IngredientsViewSet,
                    RecipeViewSet, TagViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('users', FollowViewSet)
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
