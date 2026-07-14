from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from apps.products.models import ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "parent",
        "display_order",
        "is_featured",
        "is_active",
        "products_count",
    )

    list_filter = (
        "is_featured",
        "is_active",
    )

    search_fields = (
        "title",
    )

    list_editable = (
        "display_order",
        "is_featured",
        "is_active",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    list_select_related = (
        "parent",
    )

    @admin.display(description="Products")
    def products_count(self, obj):

        count = obj.products.count()

        url = (
            reverse(
                "admin:products_product_changelist"
            )
            + f"?category__id__exact={obj.id}"
        )

        return format_html(
            '<a href="{}">{}</a>',
            url,
            count,
        )