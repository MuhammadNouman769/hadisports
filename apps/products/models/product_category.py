from django.db import models

from apps.utils.models import SlugModel


"""
===============================================================================
                            PRODUCT CATEGORY
===============================================================================

Hierarchy Example

Sports
│
├── Cricket
│   ├── Bats
│   ├── Balls
│   └── Gloves
│
├── Football
│
└── Gym Equipment

===============================================================================
"""


class ProductCategory(SlugModel):
    title = models.CharField(
        max_length=150,
        db_index=True,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        blank=True,
        null=True,
    )

    short_description = models.CharField(
        max_length=255,
        blank=True,
    )

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
    )

    display_order = models.PositiveSmallIntegerField(
        default=0,
    )

    is_featured = models.BooleanField(
        default=False,
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
            models.Index(fields=["title"]),
            models.Index(fields=["display_order"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["created_at"]),
        ]

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def is_root(self):
        return self.parent is None

    @property
    def has_children(self):
        return self.children.filter(is_active=True).exists()

    @property
    def active_products_count(self):
        return self.products.filter(is_active=True).count()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def clean(self):
        """
        Prevent assigning itself as parent.
        """

        if self.parent == self:
            from django.core.exceptions import ValidationError

            raise ValidationError(
                {"parent": "Category cannot be its own parent."}
            )

    # ------------------------------------------------------------------
    # Slug Source
    # ------------------------------------------------------------------

    def get_slug_source(self):
        return self.title

    # ------------------------------------------------------------------
    # String
    # ------------------------------------------------------------------

    def __str__(self):
        if self.parent:
            return f"{self.parent.title} → {self.title}"
        return self.title