from django.test import TestCase


class HomepageURLTests(TestCase):
    def test_homepage_url_exists(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class CoffeeEndpointTests(TestCase):
    def test_coffee_status_and_content(self):
        response = self.client.get("/coffee/")
        self.assertEqual(response.status_code, 418, "Ожидается статус 418 для /coffee")
        content = response.content.decode("utf-8")
        self.assertEqual(content, "Я чайник", "Тело ответа должно быть 'Я чайник'")
