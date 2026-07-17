from django.db import models
from apps.utils.models import BaseModel


class NewsletterSubscriber(BaseModel):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email



class HeroBanner(BaseModel):
    """
    Simple Hero Banner for homepage
    """
    title = models.CharField(
        max_length=200,
        help_text="Main heading for the banner"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Description text"
    )
    
    image = models.ImageField(
        upload_to='hero_banners/',
        help_text="Banner image (recommended: 1920x800)"
    )
    
    button_text = models.CharField(
        max_length=50,
        default="Shop Now",
        help_text="Button text"
    )
    
    
    display_order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Lower number = higher priority"
    )

    class Meta:
        db_table = "hero_banners"
        verbose_name = "Hero Banner"
        verbose_name_plural = "Hero Banners"
        ordering = ["display_order", "-created_at"]

    def __str__(self):
        return self.title
class HeroBanner(BaseModel):
    """
    Simple Hero Banner for homepage
    """
    title = models.CharField(
        max_length=200,
        help_text="Main heading for the banner"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Description text"
    )
    
    image = models.ImageField(
        upload_to='hero_banners/',
        help_text="Banner image (recommended: 1920x800)"
    )
    
    button_text = models.CharField(
        max_length=50,
        default="Shop Now",
        help_text="Button text"
    )
    
    button_url = models.CharField(
        max_length=200,
        blank=True,
        default="#",
        help_text="Button link URL"
    )
    
    display_order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Lower number = higher priority"
    )

    class Meta:
        db_table = "hero_banners"
        verbose_name = "Hero Banner"
        verbose_name_plural = "Hero Banners"
        ordering = ["display_order", "-created_at"]

    def __str__(self):
        return self.title        