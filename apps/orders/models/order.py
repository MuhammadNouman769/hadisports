from django.db import models

from apps.orders.models.adress import Address
from apps.utils.models import BaseModel
from apps.products.models.product_variant import ProductVariant

""" =================== Order =================== """   
class Order(BaseModel):
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="orders",
    )

    order_number = models.CharField(
        max_length=30,
        unique=True,
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    delivery_charges = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    notes = models.TextField(
        blank=True,
    )

    is_confirmed = models.BooleanField(
        default=False,
    )

    whatsapp_sent = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ("-created_at",)

        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["is_confirmed"]),
        ]

    def __str__(self):
        return self.order_number

    @property
    def total_items(self):
        return self.items.count()

