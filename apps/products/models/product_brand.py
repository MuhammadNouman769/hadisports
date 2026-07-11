from django.db import models

from apps.utils.models import SlugModel
from apps.utils.helpers import upload_to



# ==========================================================
# Brand
# ==========================================================

class Brand(SlugModel):
    name = models.CharField(
        max_length=150,
        unique=True,
    )

    logo = models.ImageField(
        upload_to=upload_to,
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "catalog_brands"
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["name"]

    def __str__(self):
        return self.name

