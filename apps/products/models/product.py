from django.db import models

from apps.utils.models import SlugModel
from apps.utils.helpers import upload_to
from apps.products.models.product_category import Category
from apps.products.models.product_brand import Brand


""" ====================== Product ========================= """

class Product(SlugModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=255,
    )

    sku = models.CharField(
        max_length=50,
        unique=True,
    )

    short_description = models.CharField(
        max_length=300,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    featured = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "catalog_products"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]

        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["featured"]),
            models.Index(fields=["category"]),
            models.Index(fields=["brand"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name

