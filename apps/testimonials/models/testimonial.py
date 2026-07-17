from django.db import models
from apps.utils.models import BaseModel, SlugModel


class Testimonial(BaseModel):
    """
    Testimonial model for client reviews and feedback
    """
    client_name = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Full name of the client"
    )
    
    client_profession = models.CharField(
        max_length=100,
        blank=True,
        help_text="Profession or designation of the client"
    )
    
    client_image = models.ImageField(
        upload_to='testimonials/',
        blank=True,
        null=True,
        help_text="Client profile image (recommended size: 100x100)"
    )
    
    testimonial_text = models.TextField(
        help_text="The testimonial/review text from the client"
    )
    
    rating = models.PositiveSmallIntegerField(
        default=5,
        choices=[
            (1, '1 Star'),
            (2, '2 Stars'),
            (3, '3 Stars'),
            (4, '4 Stars'),
            (5, '5 Stars'),
        ],
        help_text="Rating out of 5 stars"
    )
    
    display_order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Lower number = higher position"
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text="Check to feature this testimonial on homepage"
    )

    class Meta:
        db_table = "testimonials"
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ["display_order", "-created_at"]
        indexes = [
            models.Index(fields=["display_order"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.client_name} - {self.rating}★"

    @property
    def star_range(self):
        """Return range of stars for template looping"""
        return range(5)

    @property
    def filled_stars(self):
        """Return number of filled stars"""
        return self.rating

    @property
    def empty_stars(self):
        """Return number of empty stars"""
        return 5 - self.rating