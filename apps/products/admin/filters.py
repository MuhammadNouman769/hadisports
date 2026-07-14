from django.contrib.admin import SimpleListFilter


class StockFilter(SimpleListFilter):
    title = "Stock Status"
    parameter_name = "stock"

    def lookups(self, request, model_admin):
        return (
            ("in_stock", "In Stock"),
            ("out_of_stock", "Out of Stock"),
            ("low_stock", "Low Stock"),
        )

    def queryset(self, request, queryset):

        if self.value() == "in_stock":
            return queryset.filter(
                variants__stock_quantity__gt=0,
                variants__is_active=True,
            ).distinct()

        if self.value() == "out_of_stock":
            return queryset.filter(
                variants__stock_quantity=0,
            ).distinct()

        if self.value() == "low_stock":
            return queryset.filter(
                variants__stock_quantity__gt=0,
                variants__stock_quantity__lte=10,
            ).distinct()

        return queryset