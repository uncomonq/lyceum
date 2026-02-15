import re

from django.conf import settings

_CYRILLIC_WORD_RE = re.compile(r"\b[А-Яа-яЁё]+\b", flags=re.UNICODE)


def reverse_russian_words(text: str) -> str:
    def _rev(m: re.Match) -> str:
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

        charset = getattr(response, "charset", "utf-8") or "utf-8"
        try:
            content_text = response.content.decode(charset)
        except Exception:
            return response

        new_text = reverse_russian_words(content_text)

        if new_text == content_text:
            return response

        response.content = new_text.encode(charset)
        if response.has_header("Content-Length"):
            response["Content-Length"] = str(len(response.content))

        return response
