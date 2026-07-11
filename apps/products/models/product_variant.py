from django.db import models

from apps.utils.models import SlugModel
from apps.utils.helpers import upload_to
from apps.products.models.product_category import Category
from apps.products.models.product import Product

""" ======================== Product Variant ==================== """

class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    sku = models.CharField(
        max_length=80,
        unique=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    compare_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    quantity = models.PositiveIntegerField(
        default=0,
    )

    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
    )

    is_default = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "catalog_product_variants"
        ordering = ["id"]

        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.product.name} ({self.sku})"


# ==========================================================
# Variant Attribute
# ==========================================================

class VariantAttribute(models.Model):
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="attributes",
    )

    name = models.CharField(
        max_length=100,
    )

    value = models.CharField(
        max_length=150,
    )

    class Meta:
        db_table = "catalog_variant_attributes"
        ordering = ["id"]

    def __str__(self):
        return f"{self.name}: {self.value}"


# ==========================================================
# Variant Image
# ==========================================================

class VariantImage(models.Model):
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to=upload_to,
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        db_table = "catalog_variant_images"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.variant.product.name