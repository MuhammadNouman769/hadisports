from django.core.exceptions import ValidationError
from django.db import models

from apps.utils.models import BaseModel
from apps.products.models.product import Product
from apps.products.models.product_option import ProductOptionValue


"""
===============================================================================
                            PRODUCT VARIANT
===============================================================================

Examples

Nike Air Max

Variant 1
---------
Color : Black
Size  : 42

Price : Rs.3500

Variant 2
---------
Color : White
Size  : 43

Price : Rs.3600

===============================================================================
"""


class ProductVariant(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
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

        # Prevent duplicate option values
        if len(values) != len(set(v.pk for v in values)):
            raise ValidationError(
                "Duplicate option values are not allowed."
            )

        # Ensure option values belong to this product
        for value in values:
            if value.option.product_id != self.product_id:
                raise ValidationError(
                    f"{value} does not belong to '{self.product.name}'."
                )

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

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

    # ------------------------------------------------------------------
    # String
    # ------------------------------------------------------------------

    def __str__(self):
        return f"{self.product.name} ({self.variant_name})"