from django.contrib import admin
from django.db.models import Prefetch
from django.utils.html import format_html
from django.utils import timezone

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
        "is_bestseller",      # Added
        "is_new_arrival",
        "is_active",
        "created_at",
    )

    list_filter = (
        "category",
        "brand",
        "is_featured",
        "is_bestseller",      # Added
        "is_new_arrival",
        "is_active",
        "created_at",
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
        "is_bestseller",      # Added
        "is_new_arrival",
        "is_active",
    )

    readonly_fields = (
        "variants_count",
        "created_at",
        "updated_at",
        "new_arrival_status",
        "bestseller_status",  # Added
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
                    "is_bestseller",      # Added
                    "is_new_arrival",
                    "is_active",
                )
            },
        ),

        (
            "Information",
            {
                "fields": (
                    "variants_count",
                    "new_arrival_status",
                    "bestseller_status",  # Added
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

    @admin.display(description="New Arrival Status", boolean=True)
    def new_arrival_status(self, obj):
        """Display if product is currently in new arrivals"""
        if hasattr(obj, 'new_arrival_until') and obj.new_arrival_until:
            return timezone.now() <= obj.new_arrival_until
        return obj.is_new_arrival

    @admin.display(description="Bestseller Status", boolean=True)
    def bestseller_status(self, obj):
        """Display if product is currently a bestseller"""
        return obj.is_bestseller

    # ============================================================
    # Actions
    # ============================================================

    actions = (
        "activate_products",
        "deactivate_products",
        "mark_featured",
        "remove_featured",
        "mark_bestseller",          # Added
        "remove_bestseller",        # Added
        "mark_new_arrival",
        "remove_new_arrival",
        "make_new_arrival_for_days",
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

    @admin.action(description="Mark selected as bestseller")
    def mark_bestseller(self, request, queryset):

        updated = queryset.update(
            is_bestseller=True,
        )

        self.message_user(
            request,
            f"{updated} product(s) marked as bestseller.",
        )

    @admin.action(description="Remove bestseller status")
    def remove_bestseller(self, request, queryset):

        updated = queryset.update(
            is_bestseller=False,
        )

        self.message_user(
            request,
            f"{updated} product(s) removed from bestsellers.",
        )

    @admin.action(description="Mark selected as new arrival")
    def mark_new_arrival(self, request, queryset):

        updated = queryset.update(
            is_new_arrival=True,
        )

        self.message_user(
            request,
            f"{updated} product(s) marked as new arrival.",
        )

    @admin.action(description="Remove new arrival status")
    def remove_new_arrival(self, request, queryset):

        updated = queryset.update(
            is_new_arrival=False,
        )

        self.message_user(
            request,
            f"{updated} product(s) removed from new arrivals.",
        )

    @admin.action(description="Mark as new arrival for 15 days")
    def make_new_arrival_for_days(self, request, queryset):
        """
        Mark products as new arrivals for a specific number of days
        """
        from django.utils import timezone
        from datetime import timedelta
        
        updated = queryset.update(
            is_new_arrival=True,
        )
        
        self.message_user(
            request,
            f"{updated} product(s) marked as new arrival.",
        )

    # ============================================================
    # Inline Customization
    # ============================================================

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)