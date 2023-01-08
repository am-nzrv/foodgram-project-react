from django.db.models import F
from rest_framework import viewsets, mixins

from api.permissions import IsAdminOrReadOnly


class GetIngredientsMixin:
    """Получение ингредиентов для рецепта."""

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id', 'name', 'measurement_unit',
            mount=F('ingredients_amount__amount')
        )


class IsUserSubscribedMixin:
    """Миксина для отображения подписки на пользователя."""
    def get_is_user_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj.id).exists()


class ListRetrieveViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin):
    permission_classes = (IsAdminOrReadOnly, )


