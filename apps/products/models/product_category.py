from django.db import models

from apps.utils.models import SlugModel


""" ============================== Product Category ============================== """

class ProductCategory(SlugModel):

    class CategoryType(models.TextChoices):
        MENU = "MENU", "Menu"
        SPORT = "SPORT", "Sport"
        CATEGORY = "CATEGORY", "Category"

    title = models.CharField(
        max_length=150,
        db_index=True,
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        blank=True,
        null=True,
    )

    category_type = models.CharField(
        max_length=20,
        choices=CategoryType.choices,
        default=CategoryType.CATEGORY,
    )

    show_in_menu = models.BooleanField(
        default=False,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    short_description = models.CharField(
        max_length=255,
        blank=True,
    )

    display_order = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        db_table = "product_categories"

        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

        ordering = (
            "display_order",
            "title",
        )

        constraints = [
            models.UniqueConstraint(
                fields=["parent", "title"],
                name="unique_category_per_parent",
            )
        ]

        indexes = [
            models.Index(fields=["parent"]),
            models.Index(fields=["category_type"]),
            models.Index(fields=["show_in_menu"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["display_order"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["created_at"]),
        ]

    def get_slug_source(self):
        return self.title

    @property
    def has_children(self):
        return self.children.filter(is_active=True).exists()

    @property
    def is_root(self):
        return self.parent is None

    def __str__(self):
        return self.title