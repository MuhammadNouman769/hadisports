from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string


# =====================================================
# Soft Delete QuerySet
# =====================================================

class SoftDeleteQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)

    def delete(self):
        return self.update(is_active=False)


# =====================================================
# Base Manager
# =====================================================

class BaseManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_active=True)

    def all_objects(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


# =====================================================
# Base Model
# =====================================================

class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BaseManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def soft_delete(self):
        self.is_active = False
        self.save(update_fields=["is_active"])

    def restore(self):
        self.is_active = True
        self.save(update_fields=["is_active"])

    def __str__(self):
        return str(self.pk)


# =====================================================
# Slug Model
# =====================================================

class SlugModel(BaseModel):
    slug = models.SlugField(
        unique=True,
        blank=True,
        max_length=255,
    )

    class Meta:
        abstract = True

    def get_slug_source(self):
        """
        Override this method if slug should be generated
        from a field other than 'name'.
        """
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

            while self.__class__.all_objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)