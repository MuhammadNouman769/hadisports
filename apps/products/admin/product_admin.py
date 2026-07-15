from django.contrib import admin
from django.db.models import Prefetch
from django.utils.html import format_html

from apps.products.models import (
    Product,
    ProductVariant,
)

from .product_variant import ProductVariantInline


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    inlines = (
        ProductVariantInline,
    )

    list_display = (
        "id",
        "image_preview",
        "name",
        "category",
        "brand",
        "default_price",
        "variants_count",
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
        "short_description",
        "description",
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

    readonly_fields = (
        "variants_count",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "category",
                    "brand",
                )
            },
        ),

        (
            "Description",
            {
                "fields": (
                    "short_description",
                    "description",
                )
            },
        ),

        (
            "Settings",
            {
                "fields": (
                    "is_featured",
                    "is_active",
                )
            },
        ),

        (
            "Information",
            {
                "fields": (
                    "variants_count",
                    "created_at",
                    "updated_at",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 30

    save_on_top = True

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "category",
            )
            .prefetch_related(
                Prefetch(
                    "variants",
                    queryset=ProductVariant.objects.select_related(
                        "option1",
                        "option2",
                        "option3",
                    ),
                ),
            )
        )

    # ============================================================
    # Display Helpers
    # ============================================================

    @admin.display(description="Image")
    def image_preview(self, obj):

        image = obj.main_image

        if image and image.image:

            return format_html(
                '<img src="{}" width="70" height="70" '
                'style="object-fit:cover;border-radius:6px;">',
                image.image.url,
            )

        return "-"

    @admin.display(description="Price")
    def default_price(self, obj):

        variant = obj.default_variant

        if variant:
            return f"Rs. {variant.price}"

        return "-"

    @admin.display(description="Variants")
    def variants_count(self, obj):

        return obj.variants.filter(
            is_active=True,
        ).count()

    # ============================================================
    # Actions
    # ============================================================

    actions = (
        "activate_products",
        "deactivate_products",
        "mark_featured",
        "remove_featured",
    )

    @admin.action(description="Activate selected products")
    def activate_products(self, request, queryset):

        updated = queryset.update(
            is_active=True,
        )

        self.message_user(
            request,
            f"{updated} product(s) activated.",
        )

    @admin.action(description="Deactivate selected products")
    def deactivate_products(self, request, queryset):

        updated = queryset.update(
            is_active=False,
        )

        self.message_user(
            request,
            f"{updated} product(s) deactivated.",
        )

    @admin.action(description="Mark selected as featured")
    def mark_featured(self, request, queryset):

        updated = queryset.update(
            is_featured=True,
        )

        self.message_user(
            request,
            f"{updated} product(s) marked as featured.",
        )

    @admin.action(description="Remove featured")
    def remove_featured(self, request, queryset):

        updated = queryset.update(
            is_featured=False,
        )

        self.message_user(
            request,
            f"{updated} product(s) updated.",
        )