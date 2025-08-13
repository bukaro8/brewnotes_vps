
from django.contrib import admin
from .models import Recipe, Ingredient, DrinkType, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ['ingredient']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ('name', 'user', 'drink_type', 'created_at')
    list_filter = ('drink_type', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)


@admin.register(DrinkType)
class DrinkTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)


# @admin.register(RecipeIngredient)
# class RecipeIngredientAdmin(admin.ModelAdmin):
#     list_display = ('recipe', 'ingredient', 'quantity', 'unit')
#     list_filter = ('unit',)
