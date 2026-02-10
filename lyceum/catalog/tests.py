from django.test import TestCase


class CatalogURLTests(TestCase):
    def test_catalog_url_exists(self):
        response = self.client.get("/catalog/")
        self.assertEqual(response.status_code, 200)
