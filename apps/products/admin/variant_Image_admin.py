from django.contrib import admin
from django.utils.html import format_html

from apps.products.models import VariantImage


# ============================================================
# Variant Image Inline
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
# Variant Image Admin
# ============================================================

@admin.register(VariantImage)
class VariantImageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "variant",
        "preview",
        "position",
        "is_primary",
        "is_active",
    )

    list_filter = (
        "is_primary",
        "is_active",
        "variant__product",
    )

    search_fields = (
        "variant__product__name",
    )

    autocomplete_fields = (
        "variant",
    )

    list_editable = (
        "position",
        "is_primary",
        "is_active",
    )

    ordering = (
        "variant",
        "position",
    )

    save_on_top = True

    list_per_page = 30

    @admin.display(description="Image")
    def preview(self, obj):

        if obj.image:

            return format_html(
                '<img src="{}" width="80" height="80" '
                'style="object-fit:cover;border-radius:6px;">',
                obj.image.url,
            )

        return "-"