from .views import home, product_detail, product_list, cart, checkout, testimonial, error, error_500
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('products/', product_list, name='product-list'),
    path('checkout/', checkout, name='checkout'),
    path('product_detail/', product_detail, name='product-detail'),
    path('cart/', cart, name='cart'),
    path('testimonial/', testimonial, name='testimonial'),
    path('404/', error, name='error'),
    path('500/', error_500, name='errors'),
]