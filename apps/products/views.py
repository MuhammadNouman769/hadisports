# views.py
import json
from decimal import Decimal

from django.db.models import Prefetch, Q
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder

from apps.products.models.product import Product
from apps.products.models.product_category import ProductCategory
from apps.products.models.product_variant import ProductVariant
from apps.products.models.variant_image import VariantImage


# ==========================================================
# HOME VIEW
# ==========================================================
class HomeView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        variant_queryset = (
            ProductVariant.objects.filter(is_active=True)
            .select_related("option1", "option2", "option3")
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=VariantImage.objects.filter(is_active=True)
                    .order_by("-is_primary", "sort_order", "id"),
                ),
            )
            .order_by("-is_default", "position", "id")
        )

        product_queryset = (
            Product.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related(
                Prefetch("variants", queryset=variant_queryset),
            )
        )

        parent_categories = (
            ProductCategory.objects.filter(parent__isnull=True, is_active=True)
            .order_by("display_order", "title")[:4]
        )

        context["parent_categories"] = parent_categories

        context["featured_products"] = (
            product_queryset.filter(is_featured=True)
            .order_by("-created_at")[:8]
        )

        category_products_list = []
        for category in parent_categories:
            category_ids = [category.id]
            children = category.children.filter(is_active=True)
            category_ids.extend([child.id for child in children])
            
            products = product_queryset.filter(
                category_id__in=category_ids
            ).order_by("-created_at")[:8]
            
            category_products_list.append({
                'category': category,
                'products': products
            })
        
        context["category_products_list"] = category_products_list

        context["latest_products"] = (
            product_queryset.order_by("-created_at")[:12]
        )

        return context


# ==========================================================
# PRODUCT LIST VIEW
# ==========================================================
class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12
    
    def get_queryset(self):
        variant_queryset = (
            ProductVariant.objects.filter(is_active=True)
            .select_related("option1", "option2", "option3")
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=VariantImage.objects.filter(is_active=True)
                    .order_by("-is_primary", "sort_order", "id")[:1]
                )
            )
            .order_by("-is_default", "position", "id")
        )

        queryset = Product.objects.filter(
            is_active=True
        ).select_related(
            "category"
        ).prefetch_related(
            Prefetch("variants", queryset=variant_queryset)
        ).order_by("-created_at")
        
        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(brand__icontains=search_query) |
                Q(short_description__icontains=search_query)
            )
        
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        if min_price:
            queryset = queryset.filter(
                variants__price__gte=min_price,
                variants__is_active=True
            ).distinct()
        if max_price:
            queryset = queryset.filter(
                variants__price__lte=max_price,
                variants__is_active=True
            ).distinct()
        
        sort_by = self.request.GET.get("sort")
        if sort_by == "price_low":
            queryset = queryset.order_by("variants__price")
        elif sort_by == "price_high":
            queryset = queryset.order_by("-variants__price")
        elif sort_by == "name_asc":
            queryset = queryset.order_by("name")
        elif sort_by == "name_desc":
            queryset = queryset.order_by("-name")
        else:
            queryset = queryset.order_by("-created_at")
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["categories"] = (
            ProductCategory.objects.filter(is_active=True)
            .order_by("display_order", "title")
        )
        
        variant_queryset = (
            ProductVariant.objects.filter(is_active=True)
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=VariantImage.objects.filter(is_active=True)
                    .order_by("-is_primary", "sort_order", "id")[:1]
                )
            )
        )
        
        context["featured_products"] = (
            Product.objects.filter(is_featured=True, is_active=True)
            .prefetch_related(Prefetch("variants", queryset=variant_queryset))
            .order_by("-created_at")[:5]
        )
        
        context["current_category"] = self.request.GET.get("category", "")
        context["search_query"] = self.request.GET.get("q", "")
        context["sort_by"] = self.request.GET.get("sort", "")
        context["min_price"] = self.request.GET.get("min_price", "")
        context["max_price"] = self.request.GET.get("max_price", "")
        
        return context


# ==========================================================
# PRODUCT DETAIL VIEW
# ==========================================================
class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    
    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        
        product = get_object_or_404(
            Product.objects.filter(is_active=True).select_related("category"),
            slug=slug
        )
        
        product = Product.objects.filter(pk=product.pk).prefetch_related(
            Prefetch(
                "variants",
                queryset=ProductVariant.objects.filter(is_active=True)
                .select_related("option1__option", "option2__option", "option3__option")
                .prefetch_related(
                    Prefetch(
                        "images",
                        queryset=VariantImage.objects.filter(is_active=True)
                        .order_by("-is_primary", "sort_order", "id")
                    )
                )
                .order_by("-is_default", "position", "id")
            )
        ).first()
        
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        
        variants = product.variants.filter(is_active=True)
        
        default_variant = variants.filter(is_default=True).first()
        if not default_variant:
            default_variant = variants.first()
        
        default_image = None
        if default_variant:
            default_image = default_variant.images.filter(is_active=True).first()
        
        variants_json = []
        for variant in variants:
            variant_data = {
                "id": variant.id,
                "sku": variant.sku,
                "price": float(variant.price),
                "compare_price": float(variant.compare_price) if variant.compare_price else None,
                "discount_percentage": variant.discount_percentage,
                "stock_quantity": variant.stock_quantity,
                "is_in_stock": variant.is_in_stock,
                "option1": variant.option1_id,
                "option2": variant.option2_id,
                "option3": variant.option3_id,
                "images": [
                    {
                        "id": img.id,
                        "image": img.image.url,
                        "is_primary": img.is_primary,
                        "sort_order": img.sort_order
                    }
                    for img in variant.images.filter(is_active=True)
                ]
            }
            variants_json.append(variant_data)
        
        option_values = {}
        for variant in variants:
            for i, option in enumerate([variant.option1, variant.option2, variant.option3], 1):
                if option:
                    option_key = f"option{i}"
                    if option_key not in option_values:
                        option_values[option_key] = {}
                    
                    option_name = option.option.name
                    if option_name not in option_values[option_key]:
                        option_values[option_key][option_name] = []
                    
                    exists = False
                    for existing in option_values[option_key][option_name]:
                        if existing["id"] == option.id:
                            exists = True
                            break
                    
                    if not exists:
                        option_values[option_key][option_name].append({
                            "id": option.id,
                            "value": option.value,
                            "position": option.position,
                        })
        
        related_products = Product.objects.filter(
            category=product.category,
            is_active=True,
        ).exclude(
            pk=product.pk
        ).prefetch_related(
            Prefetch(
                "variants",
                queryset=ProductVariant.objects.filter(is_active=True)
                .select_related("option1", "option2", "option3")
                .prefetch_related(
                    Prefetch(
                        "images",
                        queryset=VariantImage.objects.filter(is_active=True)
                        .order_by("-is_primary", "sort_order", "id")
                    )
                )
            )
        ).order_by("-created_at")
        
        featured_products = Product.objects.filter(
            is_featured=True,
            is_active=True,
        ).exclude(
            pk=product.pk
        ).prefetch_related(
            Prefetch(
                "variants",
                queryset=ProductVariant.objects.filter(is_active=True)
                .select_related("option1", "option2", "option3")
                .prefetch_related(
                    Prefetch(
                        "images",
                        queryset=VariantImage.objects.filter(is_active=True)
                        .order_by("-is_primary", "sort_order", "id")
                    )
                )
            )
        ).order_by("-created_at")[:6]
        
        categories = ProductCategory.objects.filter(is_active=True).order_by("display_order", "title")
        
        context["default_variant"] = default_variant
        context["default_image"] = default_image
        context["option_values"] = option_values
        context["related_products"] = related_products
        context["featured_products"] = featured_products
        context["categories"] = categories
        context["variants_json"] = json.dumps(variants_json, cls=DjangoJSONEncoder)
        
        return context