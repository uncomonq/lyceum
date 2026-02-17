import re

from django.conf import settings

_CYRILLIC_WORD_RE = re.compile(r"\b[А-Яа-яЁё]+\b", flags=re.UNICODE)


def reverse_russian_words(text):
    def _rev(m):
        return m.group(0)[::-1]
    return _CYRILLIC_WORD_RE.sub(_rev, text)


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

        content = _CYRILLIC_WORD_RE.sub(lambda m: m.group(0)[::-1], content)

        response.content = content.encode("utf-8")
        return response
