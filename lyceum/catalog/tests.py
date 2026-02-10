from django.test import TestCase


class CatalogViewsTests(TestCase):
    def test_number_endpoint_positive_numbers(self):
        for num in ["1", "42", "123", "5", "20"]:
            response = self.client.get(f"/catalog/re/{num}/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content.decode("utf-8"), str(int(num)))

    def test_converter_endpoint_positive_numbers(self):
        for num in ["1", "42", "123", "3", "2"]:
            response = self.client.get(f"/catalog/converter/{num}/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content.decode("utf-8"), str(int(num)))

    def test_invalid_numbers(self):
        for invalid in ["0", "-1", "1.5", "abc", ""]:
            response = self.client.get(f"/catalog/re/{invalid}/")
            self.assertEqual(response.status_code, 404)
