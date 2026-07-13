from django.db import models
from apps.utils.models import BaseModel
from apps.products.models.product import Product



""" ====================== Product Option ============================= """

class ProductOption(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="options",
    )

    name = models.CharField(
        max_length=100,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        db_table = "product_options"
        verbose_name = "Product Option"
        verbose_name_plural = "Product Options"

        ordering = (
            "sort_order",
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
            models.Index(fields=["name"]),
            models.Index(fields=["sort_order"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.name}"



""" ================================ Product Option Value ================================= """

class ProductOptionValue(BaseModel):
    option = models.ForeignKey(
        ProductOption,
        on_delete=models.CASCADE,
        related_name="values",
    )

    value = models.CharField(
        max_length=100,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        db_table = "product_option_values"
        verbose_name = "Product Option Value"
        verbose_name_plural = "Product Option Values"

        ordering = (
            "sort_order",
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
            models.Index(fields=["value"]),
            models.Index(fields=["sort_order"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.option.name}: {self.value}"        