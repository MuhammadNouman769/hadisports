from django.db import models

""" ==================== Managers ================= """

class SoftDeleteQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)

    def delete(self):
        return self.update(is_active=False)

    def hard_delete(self):
        return super().delete()

    def restore(self):
        return self.update(is_active=True)


class BaseManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(
            self.model,
            using=self._db
        ).filter(is_active=True)


class AllObjectsManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(
            self.model,
            using=self._db
        )