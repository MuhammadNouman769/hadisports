from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse

from .models import Cart, CartItem
from apps.products.models.product_variant import ProductVariant


""" =================== CartView =================== """
class CartView(View):
    """Display the current user's cart"""
    template_name = "cart/cart.html"

    def get(self, request):
        cart = self.get_or_create_cart(request)
        
        # Fetch related products to show in "You May Also Like"
        related_products = []
        if cart.items.exists():
            first_item = cart.items.first()
            if first_item and first_item.variant.product.category:
                related_products = first_item.variant.product.category.products.filter(
                    is_active=True
                ).exclude(
                    id__in=[item.variant.product.id for item in cart.items.all()]
                )[:5]
        
        context = {
            'cart': cart,
            'cart_items': cart.items.all().select_related('variant__product'),
            'related_products': related_products,
        }
        return render(request, self.template_name, context)

    def get_or_create_cart(self, request):
        """Get or create cart for the current session"""
        # Ensure session exists
        if not request.session.session_key:
            request.session.save()
        
        session_key = request.session.session_key
        
        # Get or create cart
        cart, created = Cart.objects.get_or_create(
            session_key=session_key,
            defaults={'is_active': True}
        )
        
        # If cart exists but is inactive, reactivate it
        if not created and not cart.is_active:
            cart.is_active = True
            cart.save()
        
        return cart


""" =================== AddToCartView =================== """
class AddToCartView(View):
    """Add a variant to the cart (handles quantity from POST)"""
    
    def post(self, request, variant_id):
        try:
            # Get or create cart
            cart = self.get_or_create_cart(request)
            
            # Get variant
            variant = get_object_or_404(ProductVariant, id=variant_id, is_active=True)
            
            # Get quantity from POST
            quantity = int(request.POST.get('quantity', 1))
            
            # Validate quantity
            if quantity < 1:
                quantity = 1
            
            # Get or create cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, 
                variant=variant
            )
            
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            
            cart_item.save()
            
            # Check if AJAX request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f"{variant.product.name} added to cart!",
                    'cart_total_items': cart.total_items,
                    'cart_total_price': float(cart.total_price),
                    'item_quantity': cart_item.quantity,
                    'item_total': float(cart_item.total_price),
                })
            
            # Non-AJAX fallback
            messages.success(request, f"{variant.product.name} added to cart!")
            return redirect('cart:view')
            
        except ProductVariant.DoesNotExist:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'Product variant not found.'
                }, status=404)
            messages.error(request, "Product variant not found.")
            return redirect('products:product-list')
            
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f"Error: {str(e)}")
            return redirect('cart:view')

    def get_or_create_cart(self, request):
        """Get or create cart for the current session"""
        if not request.session.session_key:
            request.session.save()
        
        session_key = request.session.session_key
        
        cart, created = Cart.objects.get_or_create(
            session_key=session_key,
            defaults={'is_active': True}
        )
        
        if not created and not cart.is_active:
            cart.is_active = True
            cart.save()
        
        return cart


""" =================== UpdateCartView =================== """
class UpdateCartView(View):
    """Increase, decrease, or remove items from cart with AJAX"""
    
    def post(self, request, item_id):
        try:
            cart_item = get_object_or_404(CartItem, id=item_id)
            action = request.POST.get('action')
            
            # Perform action
            if action == 'increase':
                cart_item.quantity += 1
                cart_item.save()
                
            elif action == 'decrease':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
                    
            elif action == 'remove':
                cart_item.delete()
            
            # Get updated cart
            if cart_item.pk:
                cart = cart_item.cart
            else:
                cart = Cart.objects.get(id=cart_item.cart.id)
            
            # Calculate totals
            total_items = cart.total_items
            cart_total = float(cart.total_price)
            
            # Check if AJAX request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'new_quantity': cart_item.quantity if cart_item.pk else 0,
                    'item_total': float(cart_item.total_price) if cart_item.pk else 0,
                    'cart_total': cart_total,
                    'total_items': total_items,
                    'cart_empty': total_items == 0,
                })
            
            return redirect('cart:view')
            
        except Cart.DoesNotExist:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'Cart not found.'
                }, status=404)
            messages.error(request, "Cart not found.")
            return redirect('cart:view')
            
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f"Error: {str(e)}")
            return redirect('cart:view')


""" =================== GetCartCountView =================== """
class GetCartCountView(View):
    """AJAX endpoint to return total items in cart"""
    
    def get(self, request):
        try:
            session_key = request.session.session_key
            
            if not session_key:
                return JsonResponse({
                    'total_items': 0, 
                    'total_price': 0
                })
            
            # Get active cart
            cart = Cart.objects.filter(
                session_key=session_key, 
                is_active=True
            ).first()
            
            if not cart:
                return JsonResponse({
                    'total_items': 0, 
                    'total_price': 0
                })
            
            return JsonResponse({
                'total_items': cart.total_items,
                'total_price': float(cart.total_price)
            })
            
        except Exception as e:
            return JsonResponse({
                'total_items': 0, 
                'total_price': 0,
                'error': str(e)
            })