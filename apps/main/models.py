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
    image = models.ImageField(
        upload_to="hero_banners/",
        help_text="Banner image (recommended: 1920x800)"
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
        return f"Hero Banner #{self.pk}"