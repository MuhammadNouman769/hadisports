from django.db import models

from apps.utils.models import BaseModel
from apps.products.models.product import Product


"""
===============================================================================
                            PRODUCT OPTION
===============================================================================

Examples

Product : Nike Air Max

Options

• Color
• Size

===============================================================================
"""


class ProductOption(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="options",
    )

    name = models.CharField(
        max_length=100,
    )

    position = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        db_table = "product_options"

        verbose_name = "Product Option"
        verbose_name_plural = "Product Options"

        ordering = (
            "position",
            "id",
        )

        constraints = [
            models.UniqueConstraint(
                fields=["product", "name"],
                name="unique_product_option",
            )
        ]

        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["position"]),
            models.Index(fields=["is_active"]),
        ]

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def clean(self):
        """
        Maximum 3 options per product.
        Example:
            Color
            Size
            Material
        """

        from django.core.exceptions import ValidationError

        if not self.pk:
            count = ProductOption.objects.filter(
                product=self.product,
                is_active=True,
            ).count()

            if count >= 3:
                raise ValidationError(
                    "A product can have a maximum of 3 options."
                )

    # ------------------------------------------------------------------
    # String
    # ------------------------------------------------------------------

    def __str__(self):
        return f"{self.product.name} • {self.name}"


"""
===============================================================================
                        PRODUCT OPTION VALUE
===============================================================================

Examples

Option : Color

Values

• Black
• White
• Blue

===============================================================================
"""


class ProductOptionValue(BaseModel):
    option = models.ForeignKey(
        ProductOption,
        on_delete=models.CASCADE,
        related_name="values",
    )

    value = models.CharField(
        max_length=100,
    )

    position = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        db_table = "product_option_values"

        verbose_name = "Product Option Value"
        verbose_name_plural = "Product Option Values"

        ordering = (
            "position",
            "id",
        )

        constraints = [
            models.UniqueConstraint(
                fields=["option", "value"],
                name="unique_option_value",
            )
        ]

        indexes = [
            models.Index(fields=["option"]),
            models.Index(fields=["position"]),
            models.Index(fields=["is_active"]),
        ]

    @property
    def product(self):
        return self.option.product

    def __str__(self):
        return self.value