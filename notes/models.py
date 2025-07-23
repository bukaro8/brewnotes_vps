from django.db import models

# Create your models here.


class DrinkType(models.Model):
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
