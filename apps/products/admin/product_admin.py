from django.contrib import admin
from django.db.models import Prefetch
from django.urls import reverse
from django.utils.html import format_html

from apps.products.models import (
    Product,
    ProductVariant,
)

from .filters import StockFilter
from .product_variant import ProductVariantInline


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    inlines = (
        ProductVariantInline,
    )

    list_display = (
        "id",
        "name",
        "category",
        "brand",
        "price_range",
        "total_stock",
        "variants_count",
        "is_featured",
        "is_active",
    )

    list_filter = (
        StockFilter,
        "category",
        "brand",
        "is_featured",
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
        "slug": (
            "name",
        )
    }

    list_editable = (
        "is_featured",
        "is_active",
    )

    readonly_fields = (
        "variants_count",
        "price_range",
        "total_stock",
        "created_at",
        "updated_at",
    )

    save_on_top = True

    list_per_page = 30

    date_hierarchy = "created_at"

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
            "Statistics",
            {
                "fields": (
                    "variants_count",
                    "price_range",
                    "total_stock",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),

        (
            "Display",
            {
                "fields": (
                    "is_featured",
                    "is_active",
                )
            },
        ),

        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
    )

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

    @admin.display(description="Price")
    def price_range(self, obj):

        minimum = obj.min_price
        maximum = obj.max_price

        if minimum is None:
            return "-"

        if minimum == maximum:
            return f"Rs. {minimum}"

        return f"Rs. {minimum} - Rs. {maximum}"


    @admin.display(description="Stock")
    def total_stock(self, obj):

        stock = obj.total_stock

        if stock > 20:
            color = "#198754"

        elif stock > 5:
            color = "#fd7e14"

        elif stock > 0:
            color = "#dc3545"

        else:
            color = "#6c757d"

        return format_html(
            '<span style="color:{};font-weight:bold;">{}</span>',
            color,
            stock,
        )


    @admin.display(description="Variants")
    def variants_count(self, obj):
        return obj.variants.filter(
            is_active=True,
        ).count()


    @admin.display(description="Category")
    def category_link(self, obj):

        url = reverse(
            "admin:products_productcategory_change",
            args=[obj.category.pk],
        )

        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.category.title,
        )


    @admin.display(description="Default Variant")
    def default_variant(self, obj):

        variant = obj.default_variant

        if variant:
            return variant.variant_name

        return "-"


    @admin.display(description="Image")
    def image_preview(self, obj):

        image = obj.main_image

        if image and image.image:

            return format_html(
                '<img src="{}" '
                'width="70" '
                'height="70" '
                'style="object-fit:cover;'
                'border-radius:6px;'
                'border:1px solid #ddd;">',
                image.image.url,
            )

        return format_html(
            '<span style="color:#999;">No Image</span>'
        )


    @admin.display(description="Status")
    def stock_status(self, obj):

        if obj.total_stock == 0:

            return format_html(
                '<span style="color:#dc3545;font-weight:bold;">Out of Stock</span>'
            )

        if obj.total_stock <= 5:

            return format_html(
                '<span style="color:#fd7e14;font-weight:bold;">Low Stock</span>'
            )

        return format_html(
            '<span style="color:#198754;font-weight:bold;">In Stock</span>'
        )


    # ============================================================
    # Ordering
    # ============================================================

    ordering = (
        "-created_at",
    )

        # ============================================================
    # Actions
    # ============================================================

    actions = (
        "duplicate_products",
        "mark_featured",
        "remove_featured",
        "activate_products",
        "deactivate_products",
    )

    @admin.action(description="Duplicate selected products")
    def duplicate_products(self, request, queryset):

        duplicated = 0

        for product in queryset:

            original_variants = list(
                product.variants.all()
            )

            product.pk = None
            product.slug = None
            product.name = f"{product.name} (Copy)"
            product.is_featured = False
            product.is_active = False
            product.save()

            # Duplicate variants
            for variant in original_variants:

                variant.pk = None
                variant.product = product
                variant.is_default = False
                variant.save()

            duplicated += 1

        self.message_user(
            request,
            f"{duplicated} product(s) duplicated successfully.",
        )

    @admin.action(description="Mark as Featured")
    def mark_featured(self, request, queryset):

        updated = queryset.update(
            is_featured=True,
        )

        self.message_user(
            request,
            f"{updated} product(s) marked as featured.",
        )

    @admin.action(description="Remove Featured")
    def remove_featured(self, request, queryset):

        updated = queryset.update(
            is_featured=False,
        )

        self.message_user(
            request,
            f"{updated} product(s) updated.",
        )

    @admin.action(description="Activate Products")
    def activate_products(self, request, queryset):

        updated = queryset.update(
            is_active=True,
        )

        self.message_user(
            request,
            f"{updated} product(s) activated.",
        )

    @admin.action(description="Deactivate Products")
    def deactivate_products(self, request, queryset):

        updated = queryset.update(
            is_active=False,
        )

        self.message_user(
            request,
            f"{updated} product(s) deactivated.",
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

    # ============================================================
    # Performance
    # ============================================================

    def get_search_results(
        self,
        request,
        queryset,
        search_term,
    ):

        queryset, use_distinct = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        return queryset.distinct(), use_distinct