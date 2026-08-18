from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """
    Shows Cart items inside the Cart admin page.
    """
    model = CartItem
    extra = 0
    readonly_fields = ("variant_link", "quantity", "total_price")
    fields = ("variant_link", "quantity", "total_price")
    can_delete = True

    def variant_link(self, obj):
        """
        Creates a clickable link to the variant in the admin panel.
        """
        url = reverse(
            "admin:products_productvariant_change",
            args=[obj.variant.pk],
        )
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            url,
            obj.variant.variant_name,
        )
    variant_link.short_description = "Variant"

    def total_price(self, obj):
        return f"PKR {obj.total_price}"
    total_price.short_description = "Item Total"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Admin interface for viewing and managing guest carts.
    """
    list_display = (
        "id",
        "session_key_preview",
        "total_items",
        "total_price",
        "created_at",
        "is_active",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("session_key",)
    readonly_fields = ("session_key", "created_at", "updated_at", "total_items", "total_price")
    inlines = (CartItemInline,)
    list_per_page = 25

    fieldsets = (
        ("Cart Information", {
            "fields": ("session_key", "is_active")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
        ("Summary", {
            "fields": ("total_items", "total_price")
        }),
    )

    # ------------------------------------------------------------------
    # Display Helpers
    # ------------------------------------------------------------------

    def session_key_preview(self, obj):
        """Show only first 15 chars of the session key for cleaner display"""
        return obj.session_key[:15] + "..."
    session_key_preview.short_description = "Session Key"

    def total_items(self, obj):
        return obj.total_items
    total_items.short_description = "Total Items"

    def total_price(self, obj):
        return f"PKR {obj.total_price}"
    total_price.short_description = "Total Price"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Standalone admin for CartItem (optional, but useful for debugging).
    """
    list_display = (
        "id",
        "cart_link",
        "variant_link",
        "quantity",
        "total_price",
        "created_at",
        "is_active",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("cart__session_key", "variant__product__name")
    readonly_fields = ("cart", "variant", "quantity", "total_price")
    list_per_page = 25

    def cart_link(self, obj):
        url = reverse("admin:cart_cart_change", args=[obj.cart.pk])
        return format_html('<a href="{}" target="_blank">Cart #{}</a>', url, obj.cart.pk)
    cart_link.short_description = "Cart"

    def variant_link(self, obj):
        url = reverse("admin:products_productvariant_change", args=[obj.variant.pk])
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            url,
            obj.variant.variant_name,
        )
    variant_link.short_description = "Variant"

    def total_price(self, obj):
        return f"PKR {obj.total_price}"
    total_price.short_description = "Item Total"