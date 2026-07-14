from django.db import models
from django.db.models import Min, Max, Sum

from apps.utils.models import SlugModel
from apps.products.models.product_category import ProductCategory


"""
===============================================================================
                                PRODUCT
===============================================================================

The Product model stores only product-level information.

Examples:
---------
Nike Air Max
Samsung Galaxy S25
Adidas Football

Variant-specific information such as:

    • Price
    • Stock
    • SKU
    • Barcode
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
        """
        Return the default variant.
        If none is marked default, return the first active variant.
        """
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
    # Price Helpers
    # ------------------------------------------------------------------

    @property
    def min_price(self):
        return self.variants.filter(
            is_active=True
        ).aggregate(
            value=Min("price")
        )["value"]

    @property
    def max_price(self):
        return self.variants.filter(
            is_active=True
        ).aggregate(
            value=Max("price")
        )["value"]

    @property
    def price_range(self):
        """
        Returns:

            Rs.1000

        or

            Rs.1000 - Rs.1500
        """

        minimum = self.min_price
        maximum = self.max_price

        if minimum is None:
            return None

        if minimum == maximum:
            return minimum

        return (minimum, maximum)

    # ------------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------------

    @property
    def total_stock(self):
        return (
            self.variants.filter(
                is_active=True,
                track_inventory=True,
            ).aggregate(
                total=Sum("stock_quantity")
            )["total"]
            or 0
        )

    @property
    def is_in_stock(self):
        return self.total_stock > 0

    # ------------------------------------------------------------------
    # Images
    # ------------------------------------------------------------------

    @property
    def main_image(self):
        variant = self.default_variant

        if not variant:
            return None

        images = list(variant.images.all())

        for image in images:
            if image.is_active and image.is_primary:
                return image

        for image in images:
            if image.is_active:
                return image

        return None

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    @property
    def variants_count(self):
        return self.variants.filter(
            is_active=True,
        ).count()

    # ------------------------------------------------------------------
    # String
    # ------------------------------------------------------------------

    def __str__(self):
        return self.name