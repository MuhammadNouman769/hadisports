from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("variant", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "full_name",
        "phone",
        "total_amount",
        "created_at",
        "is_active",
    )
    list_filter = ("created_at", "is_active")
    search_fields = ("order_id", "full_name", "phone", "email")
    readonly_fields = ("order_id", "subtotal", "total_amount", "created_at", "session_key")
    inlines = (OrderItemInline,)

    fieldsets = (
        ("Order Info", {"fields": ("order_id", "session_key")}),
        ("Customer Details", {"fields": ("full_name", "email", "phone", "address", "city")}),
        ("Financials", {"fields": ("subtotal", "total_amount")}),
    )