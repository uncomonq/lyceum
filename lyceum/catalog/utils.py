import re
import unicodedata

_SIMILAR = str.maketrans(
    {
        "a": "а",
        "c": "с",
        "e": "е",
        "o": "о",
        "p": "р",
        "x": "х",
        "y": "у",
        "k": "к",
        "b": "в",
        "m": "м",
        "t": "т",
        "h": "н",
        "r": "г",
        "n": "н",
    },
)

_NON_ALNUM = re.compile(r"[^0-9a-zа-я]", re.IGNORECASE)


def normalize_name(value: str) -> str:
    if not value:
        return ""
    value = unicodedata.normalize("NFKC", value)
    value = value.lower()
    value = value.replace("ё", "е")
    value = value.translate(_SIMILAR)
    value = _NON_ALNUM.sub("", value)

    return value
