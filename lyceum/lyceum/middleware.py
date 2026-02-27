import re
import threading

from django.conf import settings

__all__ = ("ReverseRussianWordsMiddleware",)

_CYRILLIC_WORD_RE = re.compile(r"\b[А-Яа-яЁё]+\b", flags=re.UNICODE)


def _reverse_russian_words(text: str) -> str:
    return _CYRILLIC_WORD_RE.sub(lambda m: m.group(0)[::-1], text)


class ReverseRussianWordsMiddleware:
    counter = 0
    _lock = threading.Lock()
    _MOD = 10

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not getattr(settings, "ALLOW_REVERSE", True):
            return response
        with ReverseRussianWordsMiddleware._lock:
            ReverseRussianWordsMiddleware.counter = (
                ReverseRussianWordsMiddleware.counter + 1
            ) % ReverseRussianWordsMiddleware._MOD
            do_reverse = ReverseRussianWordsMiddleware.counter == 0

        if not do_reverse:
            return response

        text = response.content.decode("utf-8")
        new_text = _reverse_russian_words(text)
        response.content = new_text.encode("utf-8")
        return response
