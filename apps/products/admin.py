from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum, Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.admin import SimpleListFilter

from .models import (
    Product,
)
from apps.products.models.product_variant import (    
    ProductVariant,
    VariantImage,
    ProductOptionValue,
    VariantOptionValue,
)
from apps.products.models.product_category import (
    ProductCategory,
)
from apps.products.models.product_option import (    
    ProductOption,
)


# ============================================================
#  CUSTOM FILTERS
# ============================================================

class StockFilter(SimpleListFilter):
    """Filter products by stock status"""
    title = 'Stock Status'
    parameter_name = 'stock_status'
    
    def lookups(self, request, model_admin):
        return (
            ('in_stock', 'In Stock'),
            ('out_of_stock', 'Out of Stock'),
            ('low_stock', 'Low Stock (< 10)'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'in_stock':
            return queryset.filter(variants__stock__gt=0).distinct()
        if self.value() == 'out_of_stock':
            return queryset.filter(variants__stock=0).distinct()
        if self.value() == 'low_stock':
            return queryset.filter(variants__stock__lt=10, variants__stock__gt=0).distinct()
        return queryset


# ============================================================
#  INLINES
# ============================================================

class VariantImageInline(admin.TabularInline):
    model = VariantImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'sort_order', 'image_preview')
    readonly_fields = ('image_preview',)
    ordering = ('sort_order', 'id')
    
    def image_preview(self, obj):
        if obj and obj.image and obj.image.url:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover; border-radius:4px;" />',
                obj.image.url
            )
        return mark_safe('<span style="color:#999;">No image</span>')
    image_preview.short_description = "Preview"


class VariantOptionValueInline(admin.TabularInline):
    model = VariantOptionValue
    extra = 1
    fields = ('option_value',)
    autocomplete_fields = ('option_value',)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = (
        'id', 'option_1_value', 'option_2_value', 'option_3_value',
        'price', 'compare_price', 'stock', 'weight', 'is_default', 
        'is_active', 'variant_preview'
    )
    readonly_fields = ('variant_preview',)
    autocomplete_fields = ('option_1_value', 'option_2_value', 'option_3_value')
    
    def variant_preview(self, obj):
        if obj and obj.id:
            images = obj.images.filter(is_active=True)[:2]
            if images.exists():
                img_html = ''.join([
                    format_html(
                        '<img src="{}" width="30" height="30" style="object-fit:cover; border-radius:4px; margin:1px;" />',
                        img.image.url
                    )
                    for img in images
                ])
                return format_html('<div style="display:flex; gap:2px;">{}</div>', img_html)
            return mark_safe('<span style="color:#999;">No image</span>')
        return mark_safe('<span style="color:#999;">-</span>')
    variant_preview.short_description = "Images"


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1
    fields = ('name', 'sort_order', 'is_active')


# ============================================================
#  ADMIN CLASSES
# ============================================================

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'parent', 'category_type', 'show_in_menu', 
        'is_featured', 'is_active', 'product_count', 'display_order'
    )
    list_filter = ('category_type', 'show_in_menu', 'is_featured', 'is_active')
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('display_order', 'is_active', 'show_in_menu', 'is_featured')
    list_select_related = ('parent',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'parent', 'category_type')
        }),
        ('Display Settings', {
            'fields': ('show_in_menu', 'is_featured', 'display_order')
        }),
        ('Content', {
            'fields': ('short_description',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    @admin.display(description="Products")
    def product_count(self, obj):
        if obj:
            count = obj.products.filter(is_active=True).count()
            url = reverse('admin:products_product_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{}</a>', url, count)
        return 0
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('products')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'category', 'brand', 'price_display', 
        'stock_display', 'is_featured', 'is_active', 'created_at'
    )
    list_filter = (
        'category', 'brand', 'is_featured', 'is_active', 
        'created_at', StockFilter
    )
    search_fields = ('name', 'brand', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'is_featured')
    list_select_related = ('category',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'variant_count', 'total_stock')
    
    inlines = [ProductVariantInline, ProductOptionInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'brand')
        }),
        ('Content', {
            'fields': ('short_description', 'description')
        }),
        ('Display Settings', {
            'fields': ('is_featured',)
        }),
        ('Statistics', {
            'fields': ('variant_count', 'total_stock'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    @admin.display(description="Price")
    def price_display(self, obj):
        if obj:
            prices = obj.variants.filter(is_active=True).values_list('price', flat=True)
            if prices:
                min_price = min(prices)
                max_price = max(prices)
                if min_price == max_price:
                    return f"${min_price}"
                return f"${min_price} - ${max_price}"
        return "-"
    
    @admin.display(description="Stock")
    def stock_display(self, obj):
        if obj:
            total = obj.variants.aggregate(Sum('stock'))['stock__sum'] or 0
            if total > 50:
                color = 'green'
            elif total > 10:
                color = 'orange'
            elif total > 0:
                color = 'red'
            else:
                color = 'gray'
            return format_html(
                '<span style="color:{}; font-weight:bold;">{}</span>',
                color, total
            )
        return "-"
    
    @admin.display(description="Active Variants")
    def variant_count(self, obj):
        if obj:
            return obj.variants.filter(is_active=True).count()
        return 0
    
    @admin.display(description="Total Stock")
    def total_stock(self, obj):
        if obj:
            return obj.variants.aggregate(Sum('stock'))['stock__sum'] or 0
        return 0
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('variants')
    
    actions = ['duplicate_products', 'mark_featured', 'unmark_featured']
    
    def duplicate_products(self, request, queryset):
        for product in queryset:
            product.pk = None
            product.name = f"{product.name} (Copy)"
            product.is_active = False
            product.save()
        self.message_user(request, f"{queryset.count()} products duplicated successfully.")
    duplicate_products.short_description = "Duplicate selected products"
    
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} products marked as featured.")
    mark_featured.short_description = "Mark as featured"
    
    def unmark_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} products unmarked as featured.")
    unmark_featured.short_description = "Unmark as featured"


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product_link', 'option_display', 'price', 
        'compare_price', 'stock', 'is_default', 'is_active'
    )
    list_filter = ('is_default', 'is_active', 'product__category')
    search_fields = ('product__name',)
    list_editable = ('price', 'compare_price', 'stock', 'is_default', 'is_active')
    autocomplete_fields = ('product', 'option_1_value', 'option_2_value', 'option_3_value')
    
    inlines = [VariantImageInline, VariantOptionValueInline]
    
    fieldsets = (
        ('Product', {
            'fields': ('product',)
        }),
        ('Options', {
            'fields': ('option_1_value', 'option_2_value', 'option_3_value')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_price')
        }),
        ('Inventory', {
            'fields': ('stock', 'weight')
        }),
        ('Settings', {
            'fields': ('is_default', 'is_active')
        }),
    )
    
    @admin.display(description="Product")
    def product_link(self, obj):
        if obj and obj.product:
            url = reverse('admin:products_product_change', args=[obj.product.id])
            return format_html('<a href="{}">{}</a>', url, obj.product.name)
        return "-"
    
    @admin.display(description="Options")
    def option_display(self, obj):
        if obj:
            options = []
            if obj.option_1_value:
                options.append(str(obj.option_1_value))
            if obj.option_2_value:
                options.append(str(obj.option_2_value))
            if obj.option_3_value:
                options.append(str(obj.option_3_value))
            return " | ".join(options) if options else "-"
        return "-"
    
    actions = ['set_default', 'mark_active', 'mark_inactive']
    
    def set_default(self, request, queryset):
        queryset.update(is_default=True)
        self.message_user(request, "Selected variants set as default.")
    set_default.short_description = "Set as default"
    
    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected variants activated.")
    mark_active.short_description = "Activate variants"
    
    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected variants deactivated.")
    mark_inactive.short_description = "Deactivate variants"


@admin.register(VariantImage)
class VariantImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'variant_link', 'image_preview', 'is_primary', 'sort_order', 'is_active')
    list_filter = ('is_primary', 'is_active')
    search_fields = ('variant__product__name', 'alt_text')
    list_editable = ('is_primary', 'sort_order', 'is_active')
    autocomplete_fields = ('variant',)
    
    fieldsets = (
        ('Variant', {
            'fields': ('variant',)
        }),
        ('Image', {
            'fields': ('image', 'alt_text')
        }),
        ('Settings', {
            'fields': ('is_primary', 'sort_order', 'is_active')
        }),
    )
    
    @admin.display(description="Product")
    def variant_link(self, obj):
        if obj and obj.variant and obj.variant.product:
            return obj.variant.product.name
        return "-"
    
    @admin.display(description="Image")
    def image_preview(self, obj):
        if obj and obj.image and obj.image.url:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit:cover; border-radius:6px;" />',
                obj.image.url
            )
        return "-"


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_link', 'value_count', 'sort_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'product__name')
    list_editable = ('sort_order', 'is_active')
    autocomplete_fields = ('product',)
    
    @admin.display(description="Product")
    def product_link(self, obj):
        if obj and obj.product:
            url = reverse('admin:products_product_change', args=[obj.product.id])
            return format_html('<a href="{}">{}</a>', url, obj.product.name)
        return "-"
    
    @admin.display(description="Values")
    def value_count(self, obj):
        if obj:
            return obj.values.filter(is_active=True).count()
        return 0


@admin.register(ProductOptionValue)
class ProductOptionValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'option_link', 'sort_order', 'is_active')
    list_filter = ('is_active', 'option__name')
    search_fields = ('value', 'option__name')
    list_editable = ('sort_order', 'is_active')
    autocomplete_fields = ('option',)
    
    @admin.display(description="Option")
    def option_link(self, obj):
        if obj and obj.option:
            url = reverse('admin:products_productoption_change', args=[obj.option.id])
            return format_html('<a href="{}">{}</a>', url, obj.option.name)
        return "-"
    
    actions = ['sort_alphabetically']
    
    def sort_alphabetically(self, request, queryset):
        for option in queryset.values_list('option', flat=True).distinct():
            values = ProductOptionValue.objects.filter(option_id=option).order_by('value')
            for idx, val in enumerate(values):
                val.sort_order = idx
                val.save()
        self.message_user(request, "Values sorted alphabetically.")
    sort_alphabetically.short_description = "Sort values alphabetically"