from django.contrib import admin
from .models import DrinkType, Ingredients
# Register your models here.


@admin.register(DrinkType)
class DrinkTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
