from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.mixins import GetIsSubscribedMixin, GetIngredientsMixin
from recipes.models import (Tag, Ingredients,
                            Recipe, IngredientRecipe,
                            ShoppingCart, FavoriteRecipe)
from users.models import Follow

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password',)


class CustomUserListSerializer(GetIsSubscribedMixin, UserSerializer):
    """Сериализатор для просмотра пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')
        read_only_fields = ('is_subscribed', )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""
    class Meta:
        model = Ingredients
        fields = '__all__'


class ReadRecipeSerializer(GetIngredientsMixin,
                           serializers.ModelSerializer):
    """Сериализатор чтения рецептов."""
    tags = TagSerializer(many=True)
    author = CustomUserListSerializer()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)

    class Meta:
        model = Recipe
        fields = '__all__'


class WriteRecipeSerializer(GetIngredientsMixin,
                            serializers.ModelSerializer):
    """Cериализатор записи нового рецепта."""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author',)

    def validate(self, data):
        ingredients = self.initial_data['ingredients']
        ingredient_list = []
        if not ingredients:
            raise serializers.ValidationError(
                'Хотябы 1 ингредиент.'
            )
        for item in ingredients:
            ingredient = get_object_or_404(
                Ingredients, id=item['id']
            )
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторятся.'
                )
            if int(item.get('amount')) < 1:
                raise serializers.ValidationError(
                    'Минимальное количество = 1'
                )
            ingredient_list.append(ingredient)
        data['ingredients'] = ingredients
        return data

    def validate_cooking_time(self, time):
        if int(time) < 1:
            raise serializers.ValidationError(
                'Минимальное время = 1'
            )
        return time

    def add_ingredients_and_tags(self, instance, **validate_data):
        ingredients = validate_data['ingredients']
        tags = validate_data['tags']
        for tag in tags:
            instance.tags.add(tag)

        IngredientRecipe.objects.bulk_create([
            IngredientRecipe(
                recipe=instance,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients
        ])
        return instance

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        return self.add_ingredients_and_tags(
            recipe, ingredients=ingredients, tags=tags
        )

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = self.add_ingredients_and_tags(
            instance, ingredients=ingredients, tags=tags)
        return super().update(instance, validated_data)


class RecipeAddingSerializer(serializers.ModelSerializer):
    """Сериализатор добавления рецепта в избранное и корзину."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(GetIsSubscribedMixin, serializers.ModelSerializer):
    """Сериализатор подписки на автора."""
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = obj.author.recipes.all()
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeAddingSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.all().count()


class CheckSubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор проверки подписки на автора."""
    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate(self, obj):
        user = obj['user']
        author = obj['author']
        subscribed = user.follower.filter(author=author).exists()

        if self.context.get('request').method == 'POST':
            if user == author:
                raise serializers.ValidationError(
                    'Нельзя подписываться на себя.'
                )
            if subscribed:
                raise serializers.ValidationError(
                    'Вы уже подписаны.'
                )
        if self.context.get('request').method == 'DELETE':
            if user == author:
                raise serializers.ValidationError(
                    'Нельзя отписаться от самого себя.'
                )
            if not subscribed:
                raise serializers.ValidationError(
                    {'errors': 'Вы уже отписались от автора.'}
                )
        return obj


class CheckFavoriteRecipesSerializer(serializers.ModelSerializer):
    """Сериализатор проверки избранных рецептов."""
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )

    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')

    def validate(self, obj):
        user = self.context['request'].user
        recipe = obj['recipe']
        favorite = user.favorites.filter(recipe=recipe).exists()

        if self.context.get('request').method == 'POST' and favorite:
            raise serializers.ValidationError(
                'Рецепт уже в избранном.'
            )
        if self.context.get('request').method == 'DELETE' and not favorite:
            raise serializers.ValidationError(
                'Рецепт не в избранном.'
            )
        return obj


class CheckShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор проверки корзины."""
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def validate(self, obj):
        user = self.context['request'].user
        recipe = obj['recipe']
        cart = user.cart.filter(recipe=recipe).exists()

        if self.context.get('request').method == 'POST' and cart:
            raise serializers.ValidationError(
                'Рецепт уже в корзине.'
            )
        if self.context.get('request').method == 'DELETE' and not cart:
            raise serializers.ValidationError(
                'Рецепта нет в корзине.'
            )
        return obj
