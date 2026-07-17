from django.views.generic import TemplateView
from django.shortcuts import render
from django.templatetags.static import static
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import NewsletterSubscriber


@csrf_exempt
@require_POST
def newsletter_subscribe(request):
    email = request.POST.get('email', '').strip()
    
    if not email:
        return JsonResponse({'success': False, 'message': 'Email is required'})
    
    if NewsletterSubscriber.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'message': 'Already subscribed!'})
    
    subscriber = NewsletterSubscriber.objects.create(email=email)
    return JsonResponse({'success': True, 'message': 'Subscribed successfully!'})





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





class ServicesView(TemplateView):
    template_name = "pages/services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Service sections data
        context['service_sections'] = [
            {
                'id': 'cricket',
                'title': 'Cricket Services',
                'icon': 'fa-cricket-ball',
                'image': static('img/services/bat-service.png'),  
                'description': 'Professional cricket equipment repair and maintenance services.',
                'services': [
                    'Bat Knocking & Preparation',
                    'Bat Repairs (Cracks, Splits, Handles)',
                    'Bat Regripping',
                    'Bat Toe Guard Installation',
                    'Bat Oil Treatment',
                    'Ball Re-stitching',
                    'Pad & Glove Repair',
                    'Bat Customization (Weight/Size)'
                ]
            },
            {
                'id': 'racket',
                'title': 'Racket Sports Services',
                'icon': 'fa-table-tennis',
                'image': static('img/services/racket-service.png'),  
                'description': 'Expert racket stringing and repair for all racket sports.',
                'services': [
                    'Professional Stringing (All Tensions)',
                    'Grip Replacement (Overgrip/Replacement)',
                    'Racket Frame Repair',
                    'Grommet Replacement',
                    'Racket Balancing',
                    'String Tension Consultation',
                    'Vibration Dampener Installation'
                ]
            },
            {
                'id': 'football',
                'title': 'Football Services',
                'icon': 'fa-futbol',
                'image': static('img/services/football-service.png'),  
                'description': 'Complete football equipment repair and maintenance.',
                'services': [
                    'Ball Puncture Repair',
                    'Bladder Replacement',
                    'Stitching Repair',
                    'Ball Cleaning',
                    'Goal Net Repair',
                    'Custom Team Kit Printing'
                ]
            },
            {
                'id': 'hockey',
                'title': 'Hockey Services',
                'icon': 'fa-hockey-stick',
                'image': static('img/services/hockey-stick-service.png'),
                'description': 'Professional hockey stick repair and maintenance.',
                'services': [
                    'Stick Repair (Broken Sticks)',
                    'Grip Replacement',
                    'Blade Repair',
                    'Stick Taping',
                    'Stick Customization',
                    'Goalkeeper Equipment Repair'
                ]
            },
            {
                'id': 'boxing',
                'title': 'Boxing & MMA Services',
                'icon': 'fa-fist-raised',
                'image': static('img/services/boxing-mma.service.png'),
                'description': 'Professional boxing and MMA equipment services.',
                'services': [
                    'Glove Repair',
                    'Bag Repair',
                    'Hand Wrap Service',
                    'Glove Customization',
                    'Equipment Cleaning',
                    'Ring Installation Service'
                ]
            },
            {
                'id': 'custom',
                'title': 'Custom Services',
                'icon': 'fa-paint-brush',
                'image': static('img/services/custom-service.png'),
                'description': 'Custom sports equipment and team services.',
                'services': [
                    'Name Engraving',
                    'Custom Team Kits',
                    'Number Printing',
                    'Team Bulk Orders',
                    'Trade-in Program',
                    'Equipment Consultation'
                ]
            }
        ]
        
        return context    






class SitemapView(TemplateView):
    template_name = "pages/sitemap.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Define sitemap structure
        context['sitemap_sections'] = [
            {
                'title': 'Main Pages',
                'icon': 'fa-home',
                'links': [
                    {'name': 'Home', 'url': 'products:home-view'},
                    {'name': 'Products', 'url': 'products:product-list'},
                    {'name': 'Contact Us', 'url': 'contact:contact'},
                    {'name': 'Services', 'url': 'main:services'},
                    {'name': 'FAQ', 'url': 'main:faqs'},
                ]
            },
            {
                'title': 'Products Categories',
                'icon': 'fa-boxes',
                'links': [
                    {'name': 'Cricket Equipment', 'url': 'products:product-list', 'params': '?category=cricket'},
                    {'name': 'Badminton Equipment', 'url': 'products:product-list', 'params': '?category=badminton'},
                    {'name': 'Tennis Equipment', 'url': 'products:product-list', 'params': '?category=tennis'},
                    {'name': 'Football Equipment', 'url': 'products:product-list', 'params': '?category=football'},
                    {'name': 'Hockey Equipment', 'url': 'products:product-list', 'params': '?category=hockey'},
                    {'name': 'Boxing & MMA', 'url': 'products:product-list', 'params': '?category=boxing-mma'},
                    {'name': 'Basketball', 'url': 'products:product-list', 'params': '?category=basketball'},
                    {'name': 'Golf', 'url': 'products:product-list', 'params': '?category=golf'},
                    {'name': 'Swimming', 'url': 'products:product-list', 'params': '?category=swimming'},
                    {'name': 'Yoga', 'url': 'products:product-list', 'params': '?category=yoga'},
                    {'name': 'Running', 'url': 'products:product-list', 'params': '?category=running'},
                    {'name': 'Cycling', 'url': 'products:product-list', 'params': '?category=cycling'},
                ]
            },
            {
                'title': 'Services',
                'icon': 'fa-tools',
                'links': [
                    {'name': 'Cricket Services', 'url': 'main:services', 'anchor': 'cricket'},
                    {'name': 'Racket Sports Services', 'url': 'main:services', 'anchor': 'racket'},
                    {'name': 'Football Services', 'url': 'main:services', 'anchor': 'football'},
                    {'name': 'Hockey Services', 'url': 'main:services', 'anchor': 'hockey'},
                    {'name': 'Boxing & MMA Services', 'url': 'main:services', 'anchor': 'boxing'},
                    {'name': 'Custom Services', 'url': 'main:services', 'anchor': 'custom'},
                ]
            },
            {
                'title': 'Footwear',
                'icon': 'fa-shoe-prints',
                'links': [
                    {'name': 'Badminton Footwear', 'url': 'products:product-list', 'params': '?category=badminton-footwear'},
                    {'name': 'Cricket Footwear', 'url': 'products:product-list', 'params': '?category=cricket-footwear'},
                    {'name': 'Tennis Footwear', 'url': 'products:product-list', 'params': '?category=tennis-footwear'},
                    {'name': 'Football Footwear', 'url': 'products:product-list', 'params': '?category=football-footwear'},
                    {'name': 'Running Footwear', 'url': 'products:product-list', 'params': '?category=running-footwear'},
                    {'name': 'Golf Footwear', 'url': 'products:product-list', 'params': '?category=golf-footwear'},
                    {'name': 'Squash Footwear', 'url': 'products:product-list', 'params': '?category=squash-footwear'},
                    {'name': 'Basketball Footwear', 'url': 'products:product-list', 'params': '?category=basketball-footwear'},
                ]
            },
            {
                'title': 'Accessories',
                'icon': 'fa-cog',
                'links': [
                    {'name': 'Bags & Backpacks', 'url': 'products:product-list', 'params': '?category=bags-backpacks'},
                    {'name': 'Sports Eyewear', 'url': 'products:product-list', 'params': '?category=sports-eyewear'},
                    {'name': 'Sports Watches', 'url': 'products:product-list', 'params': '?category=sports-watches'},
                    {'name': 'Caps', 'url': 'products:product-list', 'params': '?category=caps'},
                    {'name': 'Shakers', 'url': 'products:product-list', 'params': '?category=shakers'},
                    {'name': 'Water Bottles', 'url': 'products:product-list', 'params': '?category=water-bottles'},
                    {'name': 'Headbands', 'url': 'products:product-list', 'params': '?category=headbands'},
                    {'name': 'Socks', 'url': 'products:product-list', 'params': '?category=socks'},
                    {'name': 'Towels', 'url': 'products:product-list', 'params': '?category=towels'},
                    {'name': 'Pocket Tools', 'url': 'products:product-list', 'params': '?category=pocket-tools'},
                    {'name': 'Storage', 'url': 'products:product-list', 'params': '?category=storage'},
                ]
            },
            {
                'title': 'Legal Pages',
                'icon': 'fa-gavel',
                'links': [
                    {'name': 'Privacy Policy', 'url': 'main:privacy-policy'},
                    {'name': 'Terms of Use', 'url': 'main:terms-of-use'},
                    {'name': 'Sitemap', 'url': 'main:sitemap'},
                ]
            },
        ]
        
        return context        