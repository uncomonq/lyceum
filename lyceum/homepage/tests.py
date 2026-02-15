from http import HTTPStatus

from django.test import override_settings, TestCase

from lyceum.middleware import ReverseRussianWordsMiddleware


class HomepageURLTests(TestCase):
    def test_homepage_url_exists(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)


class CoffeeEndpointTests(TestCase):
    def test_coffee_status_and_content(self):
        response = self.client.get("/coffee/")
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
        self.assertEqual(response.content.decode(), "Я чайник")


@override_settings(ALLOW_REVERSE=True)
class MiddlewareEnabledTests(TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.counter = 0

    def test_every_10th_response_is_reversed(self):
        for i in range(1, 10):
            with self.subTest(request_number=i):
                response = self.client.get("/coffee/")
                self.assertNotIn("кинйач", response.content.decode())

        response = self.client.get("/coffee/")
        self.assertIn("кинйач", response.content.decode())

    def test_multiple_tens_are_reversed(self):
        for i in range(1, 21):
            with self.subTest(request_number=i):
                response = self.client.get("/coffee/")
                content = response.content.decode()
                if i % 10 == 0:
                    self.assertIn("кинйач", content)
                else:
                    self.assertNotIn("кинйач", content)


@override_settings(ALLOW_REVERSE=False)
class MiddlewareDisabledTests(TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.counter = 0

    def test_disabled_no_reversal(self):
        for i in range(1, 21):
            with self.subTest(request_number=i):
                response = self.client.get("/coffee/")
                self.assertNotIn("кинйач", response.content.decode())
