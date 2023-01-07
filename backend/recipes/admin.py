from django.contrib import admin

from .models import (Tag, Ingredients, IngredientRecipe,
                     Recipe, FavoriteRecipe, ShoppingCart)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')


@admin.register(Ingredients)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(IngredientRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('count_favorites',)

    def count_favorites(self, obj):
        return obj.favorites.count()


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    pass
