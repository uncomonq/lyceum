from http import HTTPStatus

from django.test import override_settings, TestCase

from lyceum.middleware import ReverseRussianWordsMiddleware


class HomepageURLTests(TestCase):
    def test_homepage_url_exists(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class CoffeeEndpointTests(TestCase):
    def test_coffee_status_and_content(self):
        response = self.client.get("/coffee/")
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
        self.assertEqual(response.content.decode("utf-8"), "Я чайник")


class MiddlewareTests(TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.counter = 0

    def test_every_10th_response_is_reversed(self):
        for i in range(9):
            response = self.client.get("/coffee/")
            self.assertNotIn("кинйач", response.content.decode())
        r10 = self.client.get("/coffee/")
        self.assertIn("кинйач", r10.content.decode())


@override_settings(ALLOW_REVERSE=False)
class MiddlewareDisabledTests(TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.counter = 0

    def test_disabled_no_reversal(self):
        for _ in range(20):
            r = self.client.get("/")
            self.assertNotIn("кинйач", r.content.decode())
