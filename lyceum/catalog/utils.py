import re

_SIMILAR = str.maketrans(
    {
        "a": "а",
        "A": "а",
        "e": "е",
        "E": "е",
        "o": "о",
        "O": "о",
        "p": "р",
        "P": "р",
        "c": "с",
        "C": "с",
        "y": "у",
        "Y": "у",
        "x": "х",
        "X": "х",
        "k": "к",
        "K": "к",
        "m": "м",
        "M": "м",
        "t": "т",
        "T": "т",
        "b": "в",
        "B": "в",
        "h": "н",
        "H": "н",
    },
)

_NON_ALNUM_RE = re.compile(r"[^0-9a-zа-я]", flags=re.IGNORECASE)


def normalize_name(value: str) -> str:
    if value is None:
        value = ""
    s = str(value).strip().lower()
    s = s.translate(_SIMILAR)
    s = _NON_ALNUM_RE.sub("", s)
    return s
