from django.test import TestCase


class CatalogURLTests(TestCase):
    def test_catalog_url_exists(self):
        response = self.client.get("/catalog/")
        self.assertEqual(response.status_code, 200)


class CatalogNumberTests(TestCase):
    def test_number_endpoint_positive_numbers(self):
        # тестируем несколько положительных чисел
        for num in ["1", "42", "123456"]:
            response = self.client.get(f"/catalog/re/{num}/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content.decode("utf-8"), num)

    def test_number_endpoint_invalid_numbers(self):
        # 0 и отрицательные не должны проходить
        for invalid in ["0", "-1", "01", "abc"]:
            response = self.client.get(f"/catalog/re/{invalid}/")
            self.assertEqual(response.status_code, 404)


class CatalogConverterTests(TestCase):
    def test_converter_positive_numbers(self):
        for num in ["1", "42", "999"]:
            response = self.client.get(f"/catalog/converter/{num}/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content.decode("utf-8"), num)

    def test_converter_invalid_numbers(self):
        for invalid in ["0", "-1", "01", "1.5", "abc"]:
            response = self.client.get(f"/catalog/converter/{invalid}/")
            self.assertEqual(response.status_code, 404)
