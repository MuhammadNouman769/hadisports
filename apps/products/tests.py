from django.test import SimpleTestCase
from django.urls import reverse

from apps.products.models.product import Product


class ProjectSetupTests(SimpleTestCase):
    def test_media_url_is_standard(self):
        from django.conf import settings

        self.assertEqual(settings.MEDIA_URL, "/media/")

    def test_product_get_absolute_url_uses_product_detail_route(self):
        product = Product(name="Test Product", slug="test-product", category_id=1)
        self.assertEqual(
            product.get_absolute_url(),
            "/product/test-product/",
        )

    def test_database_default_is_sqlite_for_local_dev(self):
        from django.conf import settings

        engine = settings.DATABASES["default"]["ENGINE"]
        self.assertIn("sqlite3", engine)
