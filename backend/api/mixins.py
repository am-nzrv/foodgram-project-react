from django.db.models import F
from rest_framework import viewsets, mixins

from api.permissions import IsAdminOrReadOnly


class GetIsSubscribedMixin:
    """Миксина для отображения подписки на пользователя."""
    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj.id).exists()


class GetIngredientsMixin:
    """Получение ингредиентов для рецепта."""

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id', 'name', 'measurement_unit',
            amount=F('ingredients_amount__amount')
        )


class ListRetrieveViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin):
    permission_classes = (IsAdminOrReadOnly, )
