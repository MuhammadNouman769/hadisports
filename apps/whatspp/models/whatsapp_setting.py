from django.db import models
from apps.utils.models import BaseModel


class SiteSetting(BaseModel):
    """
    Site-wide settings that can be configured from admin
    """
    whatsapp_number = models.CharField(
        max_length=20,
        default="923248699647",
        help_text="WhatsApp number with country code (e.g., 923248699647)"
    )
    
    whatsapp_message_template = models.TextField(
        default="Hello! I'm interested in this product: {product_name}\nPrice: {price}\n\nCan you provide more details?",
        help_text="Message template for WhatsApp. Use {product_name}, {price}, {product_url} as variables."
    )
    
    site_name = models.CharField(
        max_length=100,
        default="Hadi Sports"
    )
    
    site_email = models.EmailField(
        default="info@hadisports.com"
    )
    
    site_phone = models.CharField(
        max_length=20,
        default="+92 324 869 9647"
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
                'whatsapp_number': '923248699647',
                'site_name': 'Hadi Sports'
            }
        )
        return settings