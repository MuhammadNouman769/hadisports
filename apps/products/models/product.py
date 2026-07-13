from django.db import models

from apps.utils.models import SlugModel
from apps.utils.helpers import upload_to

from apps.products.models.product_category import ProductCategory


"""======================== Product ============================"""

class Product(SlugModel):
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name="products",
    )

    brand = models.CharField(
        max_length=100,
        blank=True,
    )

    name = models.CharField(
        max_length=255,
        db_index=True,
    )


    short_description = models.CharField(
        max_length=300,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    video = models.FileField(
        upload_to=upload_to,
        blank=True,
        null=True,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "products"

        verbose_name = "Product"
        verbose_name_plural = "Products"

        ordering = (
            "name",
        )

        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["brand"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.name

    @property
    def default_variant(self):
        return self.variants.filter(
            is_default=True,
            is_active=True,
        ).first()

    @property
    def price(self):
        variant = self.default_variant
        return variant.price if variant else None

    @property
    def compare_price(self):
        variant = self.default_variant
        return variant.compare_price if variant else None

    @property
    def stock(self):
        variant = self.default_variant
        return variant.stock if variant else 0