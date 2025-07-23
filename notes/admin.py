from django.contrib import admin
from .models import DrinkType
# Register your models here.


@admin.register(DrinkType)
class DrinkTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
