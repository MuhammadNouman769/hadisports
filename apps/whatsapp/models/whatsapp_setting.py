from django.db import models
from apps.utils.models import BaseModel


class SiteSetting(BaseModel):
    """
    Site-wide settings that can be configured from admin
    """
    # WhatsApp Settings
    whatsapp_number = models.CharField(
        max_length=20,
        default="923285774948",
        help_text="WhatsApp number with country code (e.g., 923285774948 for +92 328 5774948)"
    )
    
    whatsapp_message_template = models.TextField(
        default="Hello! I'm interested in this product: {product_name}\nPrice: {price}\n\nCan you provide more details?",
        help_text="Message template for WhatsApp. Use {product_name}, {price}, {product_url} as variables."
    )
    
    # Site Information
    site_name = models.CharField(
        max_length=100,
        default="Hadi Sports"
    )
    
    site_email = models.EmailField(
        default="info@hadisports.com",
        help_text="Email address for contact form submissions"
    )
    
    site_phone = models.CharField(
        max_length=20,
        default="+92 300 1234567",
        help_text="Contact phone number"
    )
    
    site_address = models.TextField(
        default="297-C, P.I.A. Main Boulevard Road, Lahore, Pakistan"
    )
    
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return "Site Settings"
    
    @classmethod
    def get_settings(cls):
        """Get or create site settings"""
        settings, created = cls.objects.get_or_create(
            id=1,
            defaults={
                'whatsapp_number': '923285774948',
                'site_name': 'Hadi Sports',
                'site_email': 'info@hadisports.com',
                'site_phone': '+92 328 5774948',
                'site_address': '297-C, P.I.A. Main Boulevard Road, Lahore, Pakistan'
            }
        )
        return settings