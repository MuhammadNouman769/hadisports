from django.db import models

from apps.utils.models import BaseModel
from apps.products.models.product_variant import ProductVariant


""" ============== Address ================ """
class Address(BaseModel):
    full_name = models.CharField(
        max_length=150,
    )

    phone = models.CharField(
        max_length=20,
    )

    email = models.EmailField(
        blank=True,
    )

    city = models.CharField(
        max_length=100,
    )

    area = models.CharField(
        max_length=150,
        blank=True,
    )

    address = models.TextField()

    class Meta:
        db_table = "order_addresses"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        ordering = ("-created_at",)

    def __str__(self):
        return self.full_name



