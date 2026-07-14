from django.http import request
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'pages/index.html')


def product_detail(request):
    return render(request, 'products/product_detail.html')

def cart(request):
    return render(request, 'cart/cart.html')

def checkout(request):
    return render(request, 'orders/checkout.html')

def testimonial(request):
    return render(request, 'testimonials/testimonial.html')

def error(request):
    return render(request, 'errors/404.html')

def error_500(request):
    return render(request, 'errors/500.html')