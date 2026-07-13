from django.views.generic import TemplateView

from apps.products.models.product import Product
from apps.products.models.product_category import ProductCategory


class HomeView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["featured_categories"] = (
            ProductCategory.objects.filter(
                is_featured=True,
                is_active=True,
            ).order_by("display_order")
        )

        context["featured_products"] = (
            Product.objects.select_related("category")
            .prefetch_related(
                "variants",
                "variants__images",
            )
            .filter(
                is_featured=True,
                is_active=True,
            )[:12]
        )

        context["latest_products"] = (
            Product.objects.select_related("category")
            .prefetch_related(
                "variants",
                "variants__images",
            )
            .filter(
                is_active=True,
            )
            .order_by("-created_at")[:12]
        )

        return context