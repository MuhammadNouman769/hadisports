from django.urls import path
from .views import CartView, AddToCartView, UpdateCartView, GetCartCountView

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='view'),
    path('add/<int:variant_id>/', AddToCartView.as_view(), name='add'),
    path('update/<int:item_id>/', UpdateCartView.as_view(), name='update'),
    path('get-count/', GetCartCountView.as_view(), name='get_count'),  
]