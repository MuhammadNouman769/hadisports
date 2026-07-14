import os

from django.core.exceptions import ValidationError
from django.db import models

from apps.utils.helpers import upload_to
from apps.utils.models import BaseModel

from apps.products.models.product_variant import ProductVariant


"""
===============================================================================
                                VARIANT IMAGE
===============================================================================

Example

Nike Air Max

Variant
--------
Red / 42

Images
-------
front.jpg
back.jpg
side.jpg

Only one image can be primary.

===============================================================================
"""


class VariantImage(BaseModel):
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to=upload_to,
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True,
    )

    is_primary = models.BooleanField(
        default=False,
    )
    sort_order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Order of images (0 = first)"
    )

    position = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        db_table = "variant_images"

        verbose_name = "Variant Image"
        verbose_name_plural = "Variant Images"
        ordering = ("sort_order", "id") 

        ordering = (
            "position",
            "id",
        )

        indexes = [
            models.Index(fields=["variant"]),
            models.Index(fields=["position"]),
            models.Index(fields=["is_primary"]),
            models.Index(fields=["sort_order"]), 
            models.Index(fields=["is_active"]),
        ]

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def clean(self):
        if not self.image:
            raise ValidationError(
                {"image": "Image is required."}
            )

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

        if self.is_primary:
            VariantImage.objects.filter(
                variant=self.variant,
                is_primary=True,
            ).exclude(
                pk=self.pk,
            ).update(
                is_primary=False,
            )

    # ------------------------------------------------------------------
    # Delete Image File
    # ------------------------------------------------------------------

    def delete(self, *args, **kwargs):

        image_path = None

        if self.image:
            image_path = self.image.path

        super().delete(*args, **kwargs)

        if image_path and os.path.isfile(image_path):
            os.remove(image_path)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @property
    def product(self):
        return self.variant.product

    def __str__(self):
        return f"{self.variant.variant_name} Image"