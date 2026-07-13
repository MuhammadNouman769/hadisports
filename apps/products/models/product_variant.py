from django.db import models
from apps.utils.models import BaseModel
from apps.products.models.product import Product
from apps.products.models.product_option import ProductOptionValue
from apps.utils.helpers import upload_to


""" ==================== Product Variant ========================== """

class ProductVariant(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    option_1_value = models.ForeignKey(
        ProductOptionValue,
        on_delete=models.PROTECT,
        related_name="primary_variants",
        blank=True,
        null=True,
    )

    option_2_value = models.ForeignKey(
        ProductOptionValue,
        on_delete=models.PROTECT,
        related_name="secondary_variants",
        blank=True,
        null=True,
    )

    option_3_value = models.ForeignKey(
        ProductOptionValue,
        on_delete=models.PROTECT,
        related_name="tertiary_variants",
        blank=True,
        null=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    compare_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    stock = models.PositiveIntegerField(
        default=0,
    )

    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
    )

    is_default = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "product_variants"

        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"

        ordering = [
            "id",
        ]

        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["price"]),
            models.Index(fields=["stock"]),
            models.Index(fields=["is_active"]),
        ]

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def discount_amount(self):
        if self.compare_price:
            return self.compare_price - self.price
        return 0

    @property
    def discount_percentage(self):
        if self.compare_price:
            return round(
                ((self.compare_price - self.price) / self.compare_price) * 100
            )
        return 0

    def __str__(self):
        return f"{self.product.name} Variant"




""" ======================= Variant Image ========================== """

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
    )

    class Meta:
        db_table = "variant_images"

        verbose_name = "Variant Image"
        verbose_name_plural = "Variant Images"

        ordering = (
            "sort_order",
            "id",
        )

        indexes = [
            models.Index(fields=["variant"]),
            models.Index(fields=["is_primary"]),
            models.Index(fields=["sort_order"]),
            models.Index(fields=["is_active"]),
        ]

    def save(self, *args, **kwargs):
        """
        Ensure only one primary image per variant.
        """

        if self.is_primary:
            VariantImage.objects.filter(
                variant=self.variant,
                is_primary=True,
            ).exclude(
                pk=self.pk,
            ).update(
                is_primary=False,
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.variant.product.name} Image"



""" ======================== Variant Option Value ======================= """

class VariantOptionValue(BaseModel):
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="extra_options",
    )

    option_value = models.ForeignKey(
        ProductOptionValue,
        on_delete=models.PROTECT,
        related_name="variant_options",
    )

    class Meta:
        db_table = "variant_option_values"

        verbose_name = "Variant Option Value"
        verbose_name_plural = "Variant Option Values"

        ordering = (
            "id",
        )

        constraints = [
            models.UniqueConstraint(
                fields=["variant", "option_value"],
                name="unique_variant_option_value",
            )
        ]

        indexes = [
            models.Index(fields=["variant"]),
            models.Index(fields=["option_value"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.variant.product.name} - {self.option_value}"


