from django.db import models
from apps.utils.models import BaseModel
from apps.products.models.product_variant import ProductVariant

""" ==================== Cart Model ==================== """
class Cart(BaseModel):
    """
    Session-based shopping cart for guest users.
    """
    session_key = models.CharField(
        max_length=255,
        null=True,       
        blank=True,      
        db_index=True,
        help_text="Session key for guest users"
    )

    class Meta:
        db_table = "carts"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    @property
    def total_price(self):
        """Calculate total price of all items in cart"""
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        """Calculate total quantity of items in cart"""
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Cart ({self.session_key[:10]}...)" if self.session_key else "Cart (No Session)"

""" ==================== Cart Item Model ==================== """
class CartItem(BaseModel):
    """
    Individual item inside a cart.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,  #  Prevents deletion if in a cart
        related_name="cart_items",
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "cart_items"
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = (("cart", "variant"),)  # One item per variant per cart

    @property
    def total_price(self):
        """Calculate total for this item (price × quantity)"""
        return self.variant.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.variant.product.name}"