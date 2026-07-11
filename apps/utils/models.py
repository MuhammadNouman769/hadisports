import uuid

from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from .managers import BaseManager, AllObjectsManager


""" ==================== Base Models ================= """
class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    objects = BaseManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True
        ordering = ("-created_at",)

    def soft_delete(self):
        self.is_active = False
        self.save(update_fields=["is_active"])

    def restore(self):
        self.is_active = True
        self.save(update_fields=["is_active"])

    def __str__(self):
        return str(self.pk)


class UUIDModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class SlugModel(BaseModel):
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        abstract = True

    def get_slug_source(self):
        return getattr(self, "name", None)

    def save(self, *args, **kwargs):

        if not self.slug:

            source = self.get_slug_source()

            if source:
                base_slug = slugify(source)
            else:
                base_slug = get_random_string(8)

            slug = base_slug
            counter = 1

            while (
                self.__class__.all_objects
                .filter(slug=slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)