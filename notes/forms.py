from django import forms
from django.db import models
from .models import Recipe, RecipeIngredient, Ingredient
from django.contrib.auth import get_user_model


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'drink_type',
            'name',
            'description',
            'target_og',
            'target_fg',
            'fermentation_start',
            'fermentation_end',
            'coldcrash_start',
            'coldcrash_end',
            'conditioning_start',
            'conditioning_end',
            'brewing_notes',
            'testing_notes',
            'verdict',
            'image',
        ]
        widgets = {'drink_type': forms.Select(attrs={'class': 'form-select', 'id': 'id_drink_type'}),
                   'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),

                   }

        def clean_image(self):
            f = self.cleaned_data.get('image')
            if not f:
                return f
            max_mb = 10
            if getattr(f, 'size', 0) > max_mb * 1024 * 1024:
                raise forms.ValidationError(f'Image must be ≤ {max_mb}MB.')
            return f


class RecipeIngredientForm(forms.ModelForm):
    existing_ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.none(),  # start empty, fill in __init__
        required=False,
        label="Select Existing Ingredient"
    )
    new_ingredient = forms.CharField(
        max_length=100,
        required=False,
        label="Or Add New Ingredient"
    )

    class Meta:
        model = RecipeIngredient
        fields = ['existing_ingredient', 'new_ingredient', 'quantity', 'unit']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        User = get_user_model()
        admin_users = User.objects.filter(is_staff=True)

        self.fields['existing_ingredient'].queryset = Ingredient.objects.filter(
            models.Q(user=self.user) | models.Q(user__in=admin_users)
        ).distinct()

    def clean(self):
        cleaned_data = super().clean()
        existing = cleaned_data.get('existing_ingredient')
        new = cleaned_data.get('new_ingredient')

        if not existing and not new:
            raise forms.ValidationError(
                "Please select an existing ingredient or type a new one.")

        return cleaned_data

    def save(self, commit=True):
        existing = self.cleaned_data.get('existing_ingredient')
        new = self.cleaned_data.get('new_ingredient')

        if existing:
            self.instance.ingredient = existing
        else:
            self.instance.ingredient, _ = Ingredient.objects.get_or_create(
                name=new,
                user=self.user
            )
        return super().save(commit=commit)
