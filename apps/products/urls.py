from django.urls import path
from apps.products.views import HomeView, ProductListView, ProductDetailView

app_name = "products"

urlpatterns = [
    path("", HomeView.as_view(), name="home-view"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
]