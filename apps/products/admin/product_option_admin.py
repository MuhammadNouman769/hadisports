from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from apps.products.models import (
    ProductOption,
    ProductOptionValue,
)


# ============================================================
# Product Option
# ============================================================

@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "product_link",
        "position",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "product__name",
    )

    autocomplete_fields = (
        "product",
    )

    list_editable = (
        "position",
        "is_active",
    )

    ordering = (
        "product",
        "position",
    )

    save_on_top = True

    @admin.display(description="Product")
    def product_link(self, obj):

        url = reverse(
            "admin:products_product_change",
            args=[obj.product.pk],
        )

        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.product.name,
        )


# ============================================================
# Product Option Value
# ============================================================

@admin.register(ProductOptionValue)
class ProductOptionValueAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "value",
        "option",
        "product",
        "position",
        "is_active",
    )

    list_filter = (
        "option",
        "is_active",
    )

    search_fields = (
        "value",
        "option__name",
        "option__product__name",
    )

    autocomplete_fields = (
        "option",
    )

    list_editable = (
        "position",
        "is_active",
    )

    ordering = (
        "option",
        "position",
    )

    save_on_top = True

    @admin.display(description="Product")
    def product(self, obj):
        return obj.option.product