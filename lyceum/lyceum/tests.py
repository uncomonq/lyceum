from django.conf import settings
from django.test import override_settings, TestCase

import lyceum.middleware

__all__ = (
    "ReverseFunctionTests",
    "MiddlewareEnabledTests",
    "MiddlewareDisabledTests",
    "MiddlewareDefaultSettingTests",
)


class ReverseFunctionTests(TestCase):
    def test_reverse_russian_words_complex_cases(self):
        cases = {
            "Привет мир": "тевирП рим",
            "Привет, мир!": "тевирП, рим!",
            "Hello мир": "Hello рим",
            "мир123": "мир123",
            "123мир": "123мир",
            "мир-это тест": "рим-отэ тсет",
            "мир!!!": "рим!!!",
            "мирHello": "мирHello",
        }

        for original, expected in cases.items():
            with self.subTest(original=original):
                self.assertEqual(
                    lyceum.middleware._reverse_russian_words(original),
                    expected,
                )


@override_settings(ALLOW_REVERSE=True)
class MiddlewareEnabledTests(TestCase):

    def setUp(self):
        lyceum.middleware.ReverseRussianWordsMiddleware.counter = 0

    def test_10th_and_20th_are_reversed(self):
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
        lyceum.middleware.ReverseRussianWordsMiddleware.counter = 0

    def test_never_reverses_when_disabled(self):
        for i in range(1, 21):
            with self.subTest(request_number=i):
                response = self.client.get("/coffee/")
                self.assertNotIn("кинйач", response.content.decode())


class MiddlewareDefaultSettingTests(TestCase):

    def setUp(self):
        lyceum.middleware.ReverseRussianWordsMiddleware.counter = 0

    def test_behavior_matches_settings_default(self):
        for i in range(1, 11):
            response = self.client.get("/coffee/")
            content = response.content.decode()

        if getattr(settings, "ALLOW_REVERSE", False):
            self.assertIn("кинйач", content)
        else:
            self.assertNotIn("кинйач", content)
