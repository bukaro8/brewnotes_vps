from django.contrib import admin
from django import forms
from .models import DrinkType, Ingredient, Recipe
# Register your models here.


class RecipeForm(forms.ModelForm):
    # This will show a multiple-select field in the admin
    ingredient_choices = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple(
            "Ingredients", is_stacked=False),
    )

    class Meta:
        model = Recipe
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.ingredients:
            # Pre-select ingredients if they exist in the JSON list
            ingredient_ids = [ingredient.get(
                'id') for ingredient in self.instance.ingredients]
            self.fields['ingredient_choices'].initial = Ingredient.objects.filter(
                id__in=ingredient_ids)

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected_ingredients = self.cleaned_data['ingredient_choices']

        # Store as a list of {"id": X, "name": "Ingredient Name"}
        instance.ingredients = [
            {"id": ingredient.id, "name": ingredient.name}
            for ingredient in selected_ingredients
        ]

        if commit:
            instance.save()
        return instance


@admin.register(DrinkType)
class DrinkTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    form = RecipeForm  # Use the custom form
    list_display = ('name', 'user', 'drink_type')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        return (
            (None, {'fields': ('user', 'name', 'drink_type', 'verdict',)}),
            ('Ingredients', {'fields': ('ingredient_choices',)}),
            ('Description', {'fields': ('description',)}),
            ('Notes', {'fields': ('brewing_notes', 'testing_notes',)}),
            ('Details', {'fields': ('fermentation_start', 'fermentation_end',
                                    'coldcrash_start', 'coldcrash_end',
                                    'conditioning_start', 'conditioning_end',
                                    'target_og', 'target_fg')}),
        )

    def display_ingredients(self, obj):
        if not obj.ingredients:
            return "-"
        return ", ".join([ingredient['name'] for ingredient in obj.ingredients])

    display_ingredients.short_description = "Ingredients"
    list_display = ('name', 'user', 'drink_type', 'display_ingredients')
