import re

SIMILAR_LETTERS = str.maketrans({
    "a": "а",
    "e": "е",
    "o": "о",
    "p": "р",
    "c": "с",
    "y": "у",
    "x": "х",
    "k": "к",
    "m": "м",
    "t": "т",
    "b": "в",
    "h": "н",
})


def normalize_name(value: str) -> str:
    value = value.lower()
    value = value.translate(SIMILAR_LETTERS)
    value = re.sub(r"[^a-zа-я0-9]", "", value)
    return value
