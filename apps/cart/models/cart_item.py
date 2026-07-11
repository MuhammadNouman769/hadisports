
from django.db import models

from apps.cart.models.cart import Cart
from apps.utils.models import BaseModel
from apps.products.models.product_variant import ProductVariant


""" ===================== Cart Item ======================== """

class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )

    quantity = models.PositiveIntegerField(
        default=1,
    )

    class Meta:
        db_table = "cart_items"
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        ordering = ("created_at",)

        constraints = [
            models.UniqueConstraint(
                fields=["cart", "variant"],
                name="unique_cart_variant",
            )
        ]

        indexes = [
            models.Index(fields=["cart"]),
            models.Index(fields=["variant"]),
        ]

    @property
    def unit_price(self):
        return self.variant.price

    @property
    def total_price(self):
        return self.variant.price * self.quantity

    def __str__(self):
        return f"{self.variant.product.name} × {self.quantity}"