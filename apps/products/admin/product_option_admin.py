from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from apps.products.models import (
    ProductOption,
    ProductOptionValue,
)


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "product_link",
        "position",
        "is_active",
    )

    search_fields = (
        "name",
        "product__name",
    )

    list_editable = (
        "position",
        "is_active",
    )

    autocomplete_fields = (
        "product",
    )

    @admin.display(description="Product")
    def product_link(self, obj):

        url = reverse(
            "admin:products_product_change",
            args=[obj.product.id],
        )

        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.product.name,
        )


@admin.register(ProductOptionValue)
class ProductOptionValueAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "value",
        "option",
        "position",
        "is_active",
    )

    search_fields = (
        "value",
        "option__name",
    )

    autocomplete_fields = (
        "option",
    )

    list_editable = (
        "position",
        "is_active",
    )