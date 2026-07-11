
from django.db import models

from apps.utils.models import BaseModel
from apps.products.models.product_variant import ProductVariant


""" ===================== Cart ======================== """

class Cart(BaseModel):
    session_key = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    class Meta:
        db_table = "cart_carts"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["session_key"]),
            models.Index(fields=["created_at"]),
        ]

    @property
    def total_items(self):
        return self.items.count()

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return self.session_key
