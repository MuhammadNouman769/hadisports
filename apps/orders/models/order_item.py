
from django.db import models

from apps.utils.models import BaseModel
from apps.products.models.product_variant import ProductVariant
from apps.orders.models.order import Order  

""" =================== Order Item =================== """   


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        related_name="order_items",
    )

    product_name = models.CharField(
        max_length=255,
    )

    sku = models.CharField(
        max_length=80,
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    quantity = models.PositiveIntegerField()

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        db_table = "order_items"
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["variant"]),
        ]

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"