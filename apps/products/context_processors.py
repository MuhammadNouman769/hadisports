# apps/products/context_processors.py
from apps.products.models.product_category import ProductCategory


def navigation_context(request):
    """Add navigation data to all templates"""
    
    # Get all parent categories (for mega menu)
    parent_categories = ProductCategory.objects.filter(
        parent__isnull=True,
        is_active=True
    ).order_by('display_order', 'title')
    
    # Get all sub-categories
    sub_categories = ProductCategory.objects.filter(
        parent__isnull=False,
        is_active=True
    ).select_related('parent').order_by('parent__display_order', 'display_order')
    
    return {
        'nav_parent_categories': parent_categories,
        'nav_sub_categories': sub_categories,
        'cart_count': 0,
    }