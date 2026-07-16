from django.views.generic import TemplateView

from django.shortcuts import render

# Create your views here.

class TermsOfUseView(TemplateView):
    template_name = "pages/terms-of-use.html"

class PrivacyPolicyView(TemplateView):
    template_name = "pages/privacy-policy.html"

class FAQsView(TemplateView):
    template_name = "pages/faqs.html"

class CartView(TemplateView):
    template_name = "cart/cart.html"    

class CheckoutView(TemplateView):
    template_name = "orders/checkout.html"

class TestimonialView(TemplateView):
    template_name = "testimonials/testimonial.html"

class ErrorView(TemplateView):
    template_name = "errors/404.html"   

class Error500View(TemplateView):
    template_name = "errors/500.html"