from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from urllib.parse import quote
from decimal import Decimal

from apps.order.models import Order, OrderItem
from apps.cart.models import Cart
from apps.products.models.product_variant import ProductVariant
from apps.whatsapp.models.whatsapp_setting import SiteSetting
from .utils import render_to_pdf


class CheckoutView(View):
    template_name = "orders/checkout.html"

    def get(self, request):
        cart = Cart.objects.filter(session_key=request.session.session_key, is_active=True).first()
        
        if not cart or cart.items.count() == 0:
            messages.warning(request, "Your cart is empty.")
            return redirect('cart:view')

        cart_items = cart.items.all().select_related('variant__product')

        context = {
            'cart': cart,
            'cart_items': cart_items,
            'subtotal': cart.total_price,
            'total_amount': cart.total_price,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        try:
            cart = Cart.objects.filter(session_key=request.session.session_key, is_active=True).first()
            if not cart or cart.items.count() == 0:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': 'Cart is empty'}, status=400)
                messages.error(request, "Cart is empty.")
                return redirect('products:product-list')

            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            city = request.POST.get('city')

            # Validation
            if not all([full_name, phone, address, city]):
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False, 
                        'error': 'Please fill all required fields'
                    }, status=400)
                messages.error(request, "Please fill all required fields.")
                return redirect('orders:checkout')

            # Create Order
            order = Order.objects.create(
                session_key=request.session.session_key,
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                subtotal=cart.total_price,
                total_amount=cart.total_price,
            )

            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    variant=cart_item.variant,
                    quantity=cart_item.quantity,
                    price=cart_item.variant.price,
                )

            cart.is_active = False
            cart.save()

            # Generate PDF Link
            pdf_url = request.build_absolute_uri(reverse('orders:order_pdf', args=[order.order_id]))

            # Get WhatsApp number from SiteSettings
            site_settings = SiteSetting.get_settings()
            whatsapp_number = site_settings.whatsapp_number

            # Generate WhatsApp Message (Text + PDF Link)
            message = order.whatsapp_message
            message += f"\n\n📄 Download Receipt: {pdf_url}"

            encoded_msg = quote(message)
            whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_msg}"

            # Check if AJAX request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'order_id': order.order_id,
                    'whatsapp_url': whatsapp_url,
                    'pdf_url': pdf_url,
                    'message': 'Order placed successfully!'
                })

            return redirect(whatsapp_url)

        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f"Error: {str(e)}")
            return redirect('orders:checkout')


# PDF Download View (For Receipt)
class OrderPDFView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, order_id=order_id)
        pdf = render_to_pdf('orders/order_pdf.html', {'order': order})
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"Order_{order.order_id}.pdf"
            content = f"inline; filename={filename}"
            response['Content-Disposition'] = content
            return response
        return HttpResponse("PDF generation error")