__all__ = ()
import re

import unidecode

_WORD_RE = re.compile(r"\w+", re.UNICODE)


def normalize_name(value: str) -> str:
    if not value:
        return ""

    words = _WORD_RE.findall(value.lower())
    normalized = "".join(words)

    return unidecode.unidecode(normalized)
