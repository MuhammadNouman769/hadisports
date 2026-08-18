from django.urls import path
from .views import CheckoutView, OrderPDFView

app_name = 'orders'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('pdf/<str:order_id>/', OrderPDFView.as_view(), name='order_pdf'),  # ✅ PDF URL
]