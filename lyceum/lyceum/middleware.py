import re

from django.conf import settings


class ReverseRussianWordsMiddleware:
    counter = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not settings.ALLOW_REVERSE:
            return response

        ReverseRussianWordsMiddleware.counter += 1

        if ReverseRussianWordsMiddleware.counter % 10 != 0:
            return response

        content = response.content.decode("utf-8")

        def reverse_word(match):
            return match.group(0)[::-1]

        content = re.sub(r"[А-Яа-яЁё]+", reverse_word, content)

        response.content = content.encode("utf-8")
        return response
