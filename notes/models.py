from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.


class DrinkType(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='drink_types',
        help_text="Creator of this drink type"
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The name of the drink type (e.g., IPA, Stout, Lager)")
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the drink type"
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ingredients',
        help_text="Creator of this ingredient"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the ingredient"
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='recipes',
        help_text="Creator of this recipe"
    )
    drink_type = models.ForeignKey(
        'DrinkType',
        on_delete=models.PROTECT,
        related_name='recipes',
        help_text="Category of drink (e.g., IPA, Stout)"
    )
    name = models.CharField(
        max_length=200,
        help_text="Name of your recipe (e.g., 'Hoppy Summer Ale')"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the recipe"
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        related_name='recipes'
    )
    target_og = models.DecimalField(
        max_digits=4,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="Target original gravity (e.g., 1.050)"
    )
    target_fg = models.DecimalField(
        max_digits=4,
        decimal_places=3,
        null=True,
        blank=True,
        help_text="Target final gravity (e.g., 1.010)"
    )
    fermentation_start = models.DateField(
        default=timezone.now,
        null=True,
        blank=True,
        help_text="Date fermentation began (defaults to today)"
    )

    fermentation_end = models.DateField(
        null=True,
        blank=True,
        help_text="Date fermentation completed"
    )

    coldcrash_start = models.DateField(
        null=True,
        blank=True,
        help_text="Date cold crash began"
    )
    coldcrash_end = models.DateField(
        null=True,
        blank=True,
        help_text="Date cold crash completed"
    )
    conditioning_start = models.DateField(
        null=True,
        blank=True,
        help_text="Date conditioning began"
    )
    conditioning_end = models.DateField(
        null=True,
        blank=True,
        help_text="Date conditioning completed"
    )
    brewing_notes = models.TextField(
        blank=True,
        help_text="Brewing observations, adjustments, or tasting notes"
    )
    testing_notes = models.TextField(
        blank=True,
        help_text="Brewing observations, adjustments, or tasting notes"
    )
    verdict = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text="Overall rating (1=Poor, 5=Excellent)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this recipe was first created"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f"{self.name} (by {self.user.username})"


class RecipeIngredient(models.Model):
    UNIT_CHOICES = [
        ('g', 'grams'),
        ('ml', 'millilitres'),
    ]

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE
    )
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Amount of ingredient"
    )
    unit = models.CharField(
        max_length=2,
        choices=UNIT_CHOICES,
        help_text="Measurement unit"
    )

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.quantity} {self.get_unit_display()} {self.ingredient.name} for {self.recipe.name}"
