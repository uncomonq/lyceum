from http import HTTPStatus
from urllib.parse import quote

from django.test import TestCase


class CatalogViewsTests(TestCase):
    VALID_INPUTS = [
        "1",
        "01",
        "001",
        "010",
        "10",
        "100",
        "42",
        "123",
    ]

    INVALID_INPUTS = [
        "0",
        "-0",
        "-1",
        "-42",
        "1.0",
        "1.5",
        "0.1",
        "",
        "00",
        "1a",
        "a1",
        "1a2",
        "a12",
        "12a",
        "a1b2",
        "$",
        "%",
        "^",
        "@",
        "1$",
        "$1",
        "1%2",
        "abc",
    ]

    def test_re_positive_numbers(self):
        for num in self.VALID_INPUTS:
            with self.subTest(num=num):
                response = self.client.get(f"/catalog/re/{num}/")
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertEqual(
                    response.content.decode(),
                    str(int(num)),
                )

    def test_converter_positive_numbers(self):
        for num in self.VALID_INPUTS:
            with self.subTest(num=num):
                response = self.client.get(f"/catalog/converter/{num}/")
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertEqual(
                    response.content.decode(),
                    str(int(num)),
                )

    def test_re_and_converter_invalid_inputs(self):
        for inval in self.INVALID_INPUTS:
            with self.subTest(inval=inval):
                seg = quote(inval, safe="")

                resp_re = self.client.get(f"/catalog/re/{seg}/")
                self.assertEqual(resp_re.status_code, HTTPStatus.NOT_FOUND)

                resp_conv = self.client.get(f"/catalog/converter/{seg}/")
                self.assertEqual(resp_conv.status_code, HTTPStatus.NOT_FOUND)
