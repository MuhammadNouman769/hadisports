from django.db import models

from apps.utils.models import SlugModel
from apps.products.models.product_category import ProductCategory


"""
===============================================================================
                                PRODUCT
===============================================================================

Stores only product-level information.

Examples
--------
Nike Air Max
Adidas Football
Yonex Astrox 99

Variant-specific data like:

    • Price
    • Color
    • Size
    • Images

belongs to ProductVariant.

===============================================================================
"""


class Product(SlugModel):
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name="products",
    )

    name = models.CharField(
        max_length=255,
        db_index=True,
    )

    brand = models.CharField(
        max_length=100,
        blank=True,
    )

    short_description = models.CharField(
        max_length=300,
        blank=True,
    )

    description = models.TextField(
        blank=True,
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
            models.Index(fields=["category"]),
            models.Index(fields=["brand"]),
            models.Index(fields=["name"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["created_at"]),
        ]

    # ------------------------------------------------------------------
    # Variant Helpers
    # ------------------------------------------------------------------

    @property
    def has_variants(self):
        return self.variants.filter(is_active=True).exists()

    @property
    def default_variant(self):
        return (
            self.variants.filter(
                is_default=True,
                is_active=True,
            ).first()
            or self.variants.filter(
                is_active=True,
            ).first()
        )

    # ------------------------------------------------------------------
    # Main Image
    # ------------------------------------------------------------------

    @property
    def main_image(self):
        variant = self.default_variant

        if not variant:
            return None

        return variant.primary_image

    # ------------------------------------------------------------------
    # String
    # ------------------------------------------------------------------

    def __str__(self):
        return self.name