import nested_admin
from django.contrib import admin

from .models.product import Product
from .models.product_category import ProductCategory
from .models.product_option import (
    ProductOption,
    ProductOptionValue,
)
from .models.product_variant import (
    ProductVariant,
    VariantImage,
    VariantOptionValue,
)


# ==========================================================
# Product Option Value Inline
# ==========================================================

class ProductOptionValueInline(nested_admin.NestedTabularInline):
    model = ProductOptionValue
    extra = 1


# ==========================================================
# Product Option Inline
# ==========================================================

class ProductOptionInline(nested_admin.NestedStackedInline):
    model = ProductOption
    extra = 1

    inlines = [
        ProductOptionValueInline,
    ]


# ==========================================================
# Variant Image Inline
# ==========================================================

class VariantImageInline(nested_admin.NestedTabularInline):
    model = VariantImage
    extra = 1


# ==========================================================
# Product Variant Inline
# ==========================================================

class ProductVariantInline(nested_admin.NestedStackedInline):
    model = ProductVariant
    extra = 1

    inlines = [
        VariantImageInline,
    ]


# ==========================================================
# Product Category
# ==========================================================

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "parent",
        "category_type",
        "show_in_menu",
        "is_featured",
        "display_order",
        "is_active",
    )

    list_filter = (
        "category_type",
        "show_in_menu",
        "is_featured",
        "is_active",
    )

    search_fields = (
        "title",
    )

    list_editable = (
        "show_in_menu",
        "is_featured",
        "display_order",
        "is_active",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }


# ==========================================================
# Product
# ==========================================================

@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):

    list_display = (
        "name",
        "brand",
        "category",
        "price",
        "stock",
        "is_featured",
        "is_active",
    )

    list_filter = (
        "category",
        "brand",
        "is_featured",
        "is_active",
    )

    search_fields = (
        "name",
        "brand",
    )

    autocomplete_fields = (
        "category",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    list_editable = (
        "is_featured",
        "is_active",
    )

    inlines = [
        ProductOptionInline,
        ProductVariantInline,
    ]