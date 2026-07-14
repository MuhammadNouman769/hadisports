from django.contrib import admin
from django.utils.html import format_html

from apps.products.models import VariantImage


class VariantImageInline(admin.TabularInline):

    model = VariantImage

    extra = 1

    fields = (
        "image",
        "alt_text",
        "is_primary",
        "position",
        "preview",
    )

    readonly_fields = (
        "preview",
    )

    ordering = (
        "position",
    )

    def preview(self, obj):

        if obj.pk and obj.image:

            return format_html(
                '<img src="{}" width="70" style="border-radius:6px;">',
                obj.image.url,
            )

        return "-"

    preview.short_description = "Preview"


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

    list_editable = (
        "position",
        "is_primary",
        "is_active",
    )

    autocomplete_fields = (
        "variant",
    )

    def preview(self, obj):

        if obj.image:

            return format_html(
                '<img src="{}" width="80" style="border-radius:6px;">',
                obj.image.url,
            )

        return "-"

    preview.short_description = "Image"