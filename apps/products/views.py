from django.db.models import Prefetch, Q
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
import json

from apps.products.models.product import Product
from apps.products.models.product_category import ProductCategory
from apps.products.models.product_variant import ProductVariant
from apps.products.models.variant_image import VariantImage


class HomeView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ------------------------------------------------------
        # Variant Query
        # ------------------------------------------------------

        variant_queryset = (
            ProductVariant.objects.filter(is_active=True)
            .select_related("option1", "option2", "option3")
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=VariantImage.objects.filter(is_active=True)
                    .order_by("-is_primary", "position", "id"),
                ),
            )
            .order_by("-is_default", "position", "id")
        )

        # ------------------------------------------------------
        # Product Query
        # ------------------------------------------------------

        product_queryset = (
            Product.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related(
                Prefetch("variants", queryset=variant_queryset),
            )
        )

        # ------------------------------------------------------
        # Parent Categories (for featured tabs only)
        # ------------------------------------------------------

        parent_categories = (
            ProductCategory.objects.filter(
                parent__isnull=True,
                is_active=True,
            )
            .prefetch_related(
                Prefetch(
                    "children",
                    queryset=ProductCategory.objects.filter(
                        is_active=True
                    ).order_by("display_order", "title"),
                )
            )
            .order_by("display_order", "title")
        )

        featured_parent_categories = parent_categories[:4]

        context["parent_categories"] = featured_parent_categories

        # ------------------------------------------------------
        # Featured Products
        # ------------------------------------------------------

        context["featured_products"] = (
            product_queryset.filter(is_featured=True)
            .order_by("-created_at")[:8]
        )

        # ------------------------------------------------------
        # Category Wise Products (for tabs)
        # ------------------------------------------------------

        category_products_list = []

        for category in featured_parent_categories:
            category_ids = [category.id]
            category_ids.extend(
                category.children.filter(is_active=True).values_list("id", flat=True)
            )

            products = (
                product_queryset.filter(category_id__in=category_ids)
                .distinct()
                .order_by("-created_at")[:8]
            )

            category_products_list.append({
                "category": category,
                "products": products,
            })

        context["category_products_list"] = category_products_list

        # ------------------------------------------------------
        # Latest Products
        # ------------------------------------------------------

        context["latest_products"] = (
            product_queryset.order_by("-created_at")[:12]
        )

        return context


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 13

    def get_queryset(self):
        variant_queryset = (
            ProductVariant.objects.filter(is_active=True)
            .select_related("option1", "option2", "option3")
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=VariantImage.objects.filter(is_active=True)
                    .order_by("-is_primary", "position", "id"),
                ),
            )
            .order_by("-is_default", "position", "id")
        )

        queryset = (
            Product.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related(
                Prefetch("variants", queryset=variant_queryset),
            )
        )

        # Category Filter
        category_slug = self.request.GET.get("category")
        if category_slug:
            try:
                category = ProductCategory.objects.get(slug=category_slug, is_active=True)
                category_ids = [category.id]
                category_ids.extend(
                    category.children.filter(is_active=True).values_list("id", flat=True)
                )
                queryset = queryset.filter(category_id__in=category_ids)
            except ProductCategory.DoesNotExist:
                pass

        # Search
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(brand__icontains=search_query)
                | Q(short_description__icontains=search_query)
                | Q(description__icontains=search_query)
            )

        # Sorting
        sort = self.request.GET.get("sort")
        if sort == "price_low":
            queryset = queryset.order_by("variants__price")
        elif sort == "price_high":
            queryset = queryset.order_by("-variants__price")
        elif sort == "name_asc":
            queryset = queryset.order_by("name")
        elif sort == "name_desc":
            queryset = queryset.order_by("-name")
        else:
            queryset = queryset.order_by("-created_at")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        context["sort_by"] = self.request.GET.get("sort", "")
        context["category_slug"] = self.request.GET.get("category", "")
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        return get_object_or_404(
            Product.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related(
                Prefetch(
                    "variants",
                    queryset=ProductVariant.objects.filter(is_active=True)
                    .select_related("option1__option", "option2__option", "option3__option")
                    .prefetch_related(
                        Prefetch(
                            "images",
                            queryset=VariantImage.objects.filter(is_active=True)
                            .order_by("-is_primary", "position", "id"),
                        )
                    )
                    .order_by("-is_default", "position", "id"),
                )
            ),
            slug=slug,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        variants = product.variants.filter(is_active=True)

        # Default Variant
        default_variant = variants.filter(is_default=True).first()
        if not default_variant:
            default_variant = variants.first()

        default_image = None
        if default_variant:
            default_image = default_variant.images.filter(is_active=True).first()

        # Variants JSON
        variants_json = []
        for variant in variants:
            variants_json.append({
                "id": variant.id,
                "price": float(variant.price),
                "option1": variant.option1_id,
                "option2": variant.option2_id,
                "option3": variant.option3_id,
                "images": [
                    {
                        "id": image.id,
                        "image": image.image.url,
                        "is_primary": image.is_primary,
                        "position": image.position,
                    }
                    for image in variant.images.filter(is_active=True)
                ],
            })

        # Options
        option_values = {}
        for variant in variants:
            for index, option in enumerate([variant.option1, variant.option2, variant.option3], start=1):
                if not option:
                    continue
                option_key = f"option{index}"
                option_values.setdefault(option_key, {})
                option_name = option.option.name
                option_values[option_key].setdefault(option_name, [])
                exists = any(item["id"] == option.id for item in option_values[option_key][option_name])
                if not exists:
                    option_values[option_key][option_name].append({
                        "id": option.id,
                        "value": option.value,
                        "position": option.position,
                    })

        # Related Products
        related_products = (
            Product.objects.filter(category=product.category, is_active=True)
            .exclude(pk=product.pk)
            .prefetch_related(
                Prefetch(
                    "variants",
                    queryset=ProductVariant.objects.filter(is_active=True)
                    .prefetch_related(
                        Prefetch(
                            "images",
                            queryset=VariantImage.objects.filter(is_active=True)
                            .order_by("-is_primary", "position", "id"),
                        )
                    ),
                )
            )
            .order_by("-created_at")[:8]
        )

        # Featured Products
        featured_products = (
            Product.objects.filter(is_featured=True, is_active=True)
            .exclude(pk=product.pk)
            .prefetch_related(
                Prefetch(
                    "variants",
                    queryset=ProductVariant.objects.filter(is_active=True)
                    .prefetch_related(
                        Prefetch(
                            "images",
                            queryset=VariantImage.objects.filter(is_active=True)
                            .order_by("-is_primary", "position", "id"),
                        )
                    ),
                )
            )
            .order_by("-created_at")[:6]
        )

        context["default_variant"] = default_variant
        context["default_image"] = default_image
        context["option_values"] = option_values
        context["related_products"] = related_products
        context["featured_products"] = featured_products
        context["variants_json"] = json.dumps(variants_json, cls=DjangoJSONEncoder)

        return context