from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from apps.utils.models import BaseModel
from apps.products.models.product import Product
from apps.products.models.product_option import ProductOptionValue


"""
===============================================================================
                            PRODUCT VARIANT
===============================================================================

Example

Nike Air Max

Variant 1
---------
Color  : Red
Size   : 42

Variant 2
---------
Color  : Blue
Size   : 43

===============================================================================
"""


class ProductVariant(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
        blank=True,  # Allow blank for auto-generation
    )

    barcode = models.CharField(
        max_length=100,
        blank=True,
    )

    option1 = models.ForeignKey(
        ProductOptionValue,
        on_delete=models.PROTECT,
        related_name="variants_option1",
        blank=True,
        null=True,
    )

    option2 = models.ForeignKey(
        ProductOptionValue,
        on_delete=models.PROTECT,
        related_name="variants_option2",
        blank=True,
        null=True,
    )

    option3 = models.ForeignKey(
        ProductOptionValue,
        on_delete=models.PROTECT,
        related_name="variants_option3",
        blank=True,
        null=True,
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    compare_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )

    stock_quantity = models.PositiveIntegerField(
        default=0,
    )

    track_inventory = models.BooleanField(
        default=True,
    )

    allow_backorder = models.BooleanField(
        default=False,
    )

    is_default = models.BooleanField(
        default=False,
    )

    position = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        db_table = "product_variants"

        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"

        ordering = (
            "position",
            "id",
        )

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "product",
                    "option1",
                    "option2",
                    "option3",
                ],
                name="unique_product_variant",
            )
        ]

        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["price"]),
            models.Index(fields=["is_default"]),
            models.Index(fields=["is_active"]),
        ]

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def clean(self):
        values = [
            value
            for value in [self.option1, self.option2, self.option3]
            if value
        ]

        # Duplicate option values
        if len(values) != len(set(v.pk for v in values)):
            raise ValidationError(
                "A variant cannot contain duplicate option values."
            )

        # Ensure option values belong to same product
        for value in values:
            if value.option.product_id != self.product_id:
                raise ValidationError(
                    f"{value} does not belong to '{self.product.name}'."
                )

        # compare price validation
        if (
            self.compare_price
            and self.compare_price <= self.price
        ):
            raise ValidationError(
                {
                    "compare_price":
                    "Compare price must be greater than price."
                }
            )

    # ------------------------------------------------------------------
    # Auto-Generate SKU
    # ------------------------------------------------------------------

    def generate_sku(self):
        """
        Auto-generate SKU based on product ID and option values
        Format: SKU-{product_id}-{option_ids}
        """
        # Get option values
        option_values = []
        for value in [self.option1, self.option2, self.option3]:
            if value:
                option_values.append(str(value.id))
        
        # Generate base SKU
        if option_values:
            base_sku = f"SKU-{self.product_id}-{'-'.join(option_values)}"
        else:
            # For variants without options (simple products)
            base_sku = f"SKU-{self.product_id}-DEFAULT"
        
        # Ensure uniqueness
        sku = base_sku
        counter = 1
        
        # Check if SKU already exists (excluding current instance if it exists)
        while ProductVariant.objects.filter(sku=sku).exclude(pk=self.pk).exists():
            sku = f"{base_sku}-{counter}"
            counter += 1
        
        return sku

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save(self, *args, **kwargs):
        # Auto-generate SKU if not provided
        if not self.sku:
            self.sku = self.generate_sku()

        self.full_clean()

        super().save(*args, **kwargs)

        # only one default variant
        if self.is_default:
            ProductVariant.objects.filter(
                product=self.product,
            ).exclude(
                pk=self.pk,
            ).update(
                is_default=False,
            )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @property
    def option_values(self):
        return [
            value
            for value in [self.option1, self.option2, self.option3]
            if value
        ]

    @property
    def variant_name(self):
        if not self.option_values:
            return "Default"

        return " / ".join(
            value.value for value in self.option_values
        )

    @property
    def is_in_stock(self):

        if not self.track_inventory:
            return True

        if self.allow_backorder:
            return True

        return self.stock_quantity > 0

    @property
    def discount_amount(self):

        if not self.compare_price:
            return Decimal("0.00")

        return self.compare_price - self.price

    @property
    def discount_percentage(self):

        if not self.compare_price:
            return 0

        return round(
            (
                (self.compare_price - self.price)
                / self.compare_price
            )
            * 100
        )

    @property
    def primary_image(self):
        image = self.images.filter(
            is_primary=True,
            is_active=True,
        ).first()

        if image:
            return image

        return self.images.filter(
            is_active=True,
        ).first()

    def __str__(self):
        return f"{self.product.name} ({self.variant_name})"