from django.contrib import admin
from django.utils.html import format_html

from apps.products.models import (
    ProductVariant,
    VariantImage,
)


# ============================================================
# Variant Images Inline
# ============================================================

class VariantImageInline(admin.TabularInline):

    model = VariantImage

    extra = 1

    fields = (
        "image",
        "is_primary",
        "position",
        "preview",
    )

    readonly_fields = (
        "preview",
    )

    ordering = (
        "position",
        "id",
    )

    def preview(self, obj):

        if obj.pk and obj.image:

            return format_html(
                '<img src="{}" width="70" height="70" '
                'style="object-fit:cover;border-radius:6px;">',
                obj.image.url,
            )

        return "-"

    preview.short_description = "Preview"


# ============================================================
# Product Variant Inline
# ============================================================

class ProductVariantInline(admin.TabularInline):

    model = ProductVariant

    extra = 1

    show_change_link = True

    autocomplete_fields = (
        "option1",
        "option2",
        "option3",
    )

    fields = (
        "option1",
        "option2",
        "option3",
        "price",
        "is_default",
        "position",
        "is_active",
    )


# ============================================================
# Product Variant Admin
# ============================================================

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "variant_name",
        "price",
        "image_preview",
        "is_default",
        "is_active",
    )

    list_filter = (
        "product__category",
        "is_default",
        "is_active",
    )

    search_fields = (
        "product__name",
    )

    autocomplete_fields = (
        "product",
        "option1",
        "option2",
        "option3",
    )

    list_editable = (
        "price",
        "is_default",
        "is_active",
    )

    readonly_fields = (
        "variant_name",
    )

    inlines = (
        VariantImageInline,
    )

    fieldsets = (
        (
            "Product",
            {
                "fields": (
                    "product",
                ),
            },
        ),

        (
            "Variant Options",
            {
                "fields": (
                    "option1",
                    "option2",
                    "option3",
                ),
            },
        ),

        (
            "Pricing",
            {
                "fields": (
                    "price",
                ),
            },
        ),

        (
            "Settings",
            {
                "fields": (
                    "position",
                    "is_default",
                    "is_active",
                ),
            },
        ),
    )

    ordering = (
        "product",
        "position",
    )

    save_on_top = True

    list_per_page = 30

    # ============================================================
    # Display Helpers
    # ============================================================

    @admin.display(description="Image")
    def image_preview(self, obj):

        image = obj.primary_image

        if image and image.image:

            return format_html(
                '<img src="{}" width="70" height="70" '
                'style="object-fit:cover;border-radius:6px;">',
                image.image.url,
            )

        return "-"

    # ============================================================
    # Actions
    # ============================================================

    actions = (
        "make_default",
        "activate_variants",
        "deactivate_variants",
    )

    @admin.action(description="Set selected variants as default")
    def make_default(self, request, queryset):

        updated = 0

        for variant in queryset:

            ProductVariant.objects.filter(
                product=variant.product,
            ).update(
                is_default=False,
            )

            variant.is_default = True
            variant.save()

            updated += 1

        self.message_user(
            request,
            f"{updated} variant(s) updated.",
        )

    @admin.action(description="Activate selected variants")
    def activate_variants(self, request, queryset):

        count = queryset.update(
            is_active=True,
        )

        self.message_user(
            request,
            f"{count} variant(s) activated.",
        )

    @admin.action(description="Deactivate selected variants")
    def deactivate_variants(self, request, queryset):

        count = queryset.update(
            is_active=False,
        )

        self.message_user(
            request,
            f"{count} variant(s) deactivated.",
        )