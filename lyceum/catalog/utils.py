import re


_SIMILAR = str.maketrans({
    "a": "а", "A": "а",
    "b": "б", "B": "б",
    "c": "с", "C": "с",
    "d": "д", "D": "д",
    "e": "е", "E": "е",
    "f": "ф", "F": "ф",
    "g": "г", "G": "г",
    "h": "н", "H": "н",
    "i": "и", "I": "и",
    "j": "й", "J": "й",
    "k": "к", "K": "к",
    "l": "л", "L": "л",
    "m": "м", "M": "м",
    "n": "н", "N": "н",
    "o": "о", "O": "о",
    "p": "р", "P": "р",
    "q": "я", "Q": "я",
    "r": "р", "R": "р",
    "s": "с", "S": "с",
    "t": "т", "T": "т",
    "u": "у", "U": "у",
    "v": "в", "V": "в",
    "w": "в", "W": "в",
    "x": "х", "X": "х",
    "y": "у", "Y": "у",
    "z": "з", "Z": "з",
    },
)

_NON_ALNUM_RE = re.compile(r"[^0-9a-zа-яё]", flags=re.IGNORECASE)


def normalize_name(value: str) -> str:
    if value is None:
        value = ""
    s = str(value).strip().lower()
    s = s.translate(_SIMILAR)
    s = _NON_ALNUM_RE.sub("", s)
    return s
