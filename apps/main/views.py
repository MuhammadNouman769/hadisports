from django.views.generic import TemplateView
from django.shortcuts import render
from django.templatetags.static import static
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



from django.views.generic import TemplateView


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