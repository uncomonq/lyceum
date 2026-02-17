import re

from django.core.exceptions import ValidationError

KEYWORD_RE = re.compile(
    r"\b(превосходно|роскошно)\b", flags=re.IGNORECASE | re.UNICODE,
)


def validate_keywords(value):
    if not KEYWORD_RE.search(value):
        raise ValidationError(
            "Текст должен содержать слово «превосходно» или «роскошно».",
        )
