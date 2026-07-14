from django.contrib import admin
from django.db.models import Prefetch
from django.urls import reverse
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
# Product Variant Inline (Used in Product Admin)
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
        "compare_price",
        "stock_quantity",
        "track_inventory",
        "allow_backorder",
        "is_default",
        "is_active",
    )


# ============================================================
# Product Variant Admin
# ============================================================

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product_link",
        "variant_name",
        "price",
        "compare_price",
        "stock_display",
        "is_default",
        "is_active",
    )

    list_filter = (
        "is_default",
        "track_inventory",
        "allow_backorder",
        "is_active",
        "product__category",
    )

    search_fields = (
        "product__name",
        "sku",
        "barcode",
    )

    autocomplete_fields = (
        "product",
        "option1",
        "option2",
        "option3",
    )

    list_editable = (
        "price",
        "compare_price",
        "is_default",
        "is_active",
    )

    readonly_fields = (
        "variant_name",
        "discount_percentage",
        "discount_amount",
        "is_in_stock",
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
                )
            },
        ),

        (
            "Variant Options",
            {
                "fields": (
                    "option1",
                    "option2",
                    "option3",
                )
            },
        ),

        (
            "Pricing",
            {
                "fields": (
                    "price",
                    "compare_price",
                    "discount_amount",
                    "discount_percentage",
                )
            },
        ),

        (
            "Inventory",
            {
                "fields": (
                    "stock_quantity",
                    "track_inventory",
                    "allow_backorder",
                    "is_in_stock",
                )
            },
        ),

        (
            "Identification",
            {
                "fields": (
                    "sku",
                    "barcode",
                )
            },
        ),

        (
            "Settings",
            {
                "fields": (
                    "position",
                    "is_default",
                    "is_active",
                )
            },
        ),
    )

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "product",
                "option1",
                "option2",
                "option3",
            )
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=VariantImage.objects.filter(
                        is_active=True,
                    ),
                )
            )
        )
    
        # ============================================================
    # Display Helpers
    # ============================================================

    @admin.display(description="Product")
    def product_link(self, obj):

        url = reverse(
            "admin:products_product_change",
            args=[obj.product.pk],
        )

        return format_html(
            '<a href="{}"><strong>{}</strong></a>',
            url,
            obj.product.name,
        )

    @admin.display(description="Variant")
    def variant_name(self, obj):
        return obj.variant_name

    @admin.display(description="Stock")
    def stock_display(self, obj):

        if not obj.track_inventory:
            return format_html(
                '<span style="color:#0d6efd;font-weight:bold;">Unlimited</span>'
            )

        if obj.allow_backorder:
            return format_html(
                '<span style="color:#198754;font-weight:bold;">{} (Backorder)</span>',
                obj.stock_quantity,
            )

        if obj.stock_quantity > 20:
            color = "#198754"

        elif obj.stock_quantity > 5:
            color = "#fd7e14"

        elif obj.stock_quantity > 0:
            color = "#dc3545"

        else:
            color = "#6c757d"

        return format_html(
            '<span style="color:{};font-weight:bold;">{}</span>',
            color,
            obj.stock_quantity,
        )

    @admin.display(description="Discount")
    def discount(self, obj):

        if not obj.compare_price:
            return "-"

        return "{}%".format(
            obj.discount_percentage,
        )

    @admin.display(description="Primary Image")
    def image_preview(self, obj):

        image = obj.primary_image

        if image and image.image:

            return format_html(
                '<img src="{}" '
                'width="70" '
                'height="70" '
                'style="object-fit:cover;border-radius:6px;border:1px solid #ddd;">',
                image.image.url,
            )

        return format_html(
            '<span style="color:#999;">No Image</span>'
        )

    @admin.display(description="Options")
    def option_display(self, obj):

        values = []

        if obj.option1:
            values.append(
                f"{obj.option1.option.name}: {obj.option1.value}"
            )

        if obj.option2:
            values.append(
                f"{obj.option2.option.name}: {obj.option2.value}"
            )

        if obj.option3:
            values.append(
                f"{obj.option3.option.name}: {obj.option3.value}"
            )

        if not values:
            return "-"

        return format_html(
            "<br>".join(values)
        )

    # ============================================================
    # Ordering
    # ============================================================

    ordering = (
        "product",
        "position",
        "id",
    )

    list_per_page = 30

    save_on_top = True


        # ============================================================
    # Actions
    # ============================================================

    actions = (
        "make_default",
        "activate_variants",
        "deactivate_variants",
        "enable_inventory_tracking",
        "disable_inventory_tracking",
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
            variant.save(update_fields=["is_default"])

            updated += 1

        self.message_user(
            request,
            f"{updated} variant(s) marked as default.",
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

    @admin.action(description="Enable inventory tracking")
    def enable_inventory_tracking(self, request, queryset):

        count = queryset.update(
            track_inventory=True,
        )

        self.message_user(
            request,
            f"Inventory tracking enabled for {count} variant(s).",
        )

    @admin.action(description="Disable inventory tracking")
    def disable_inventory_tracking(self, request, queryset):

        count = queryset.update(
            track_inventory=False,
        )

        self.message_user(
            request,
            f"Inventory tracking disabled for {count} variant(s).",
        )

    # ============================================================
    # Save
    # ============================================================

    def save_model(self, request, obj, form, change):

        super().save_model(
            request,
            obj,
            form,
            change,
        )

        # Ensure only one default variant per product.
        if obj.is_default:

            ProductVariant.objects.filter(
                product=obj.product,
            ).exclude(
                pk=obj.pk,
            ).update(
                is_default=False,
            )

    # ============================================================
    # Permissions
    # ============================================================

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj)

    # ============================================================
    # Optimizations
    # ============================================================

    def get_readonly_fields(self, request, obj=None):

        readonly = list(self.readonly_fields)

        if obj:
            readonly.append("variant_name")

        return readonly