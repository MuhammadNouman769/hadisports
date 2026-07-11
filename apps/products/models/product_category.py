from django.db import models

from apps.utils.models import SlugModel
from apps.utils.helpers import upload_to


# ==========================================================
# Category
# ==========================================================

class Category(SlugModel):
    name = models.CharField(
        max_length=150,
        unique=True,
    )

    image = models.ImageField(
        upload_to=upload_to,
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        db_table = "catalog_categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["sort_order", "name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name

