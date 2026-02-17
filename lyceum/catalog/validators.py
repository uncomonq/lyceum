import re

from django.core.exceptions import ValidationError


class ValidateMustContain:
    def deconstruct(self):
        path = "catalog.validators.ValidateMustContain"
        args = self.words
        kwargs = {}
        return path, args, kwargs

    message = "Текст должен содержать хотя бы одно из слов: {words}."
    code = "must_contain"

    def __init__(self, *words):
        if not words:
            raise ValueError("Необходимо передать хотя бы одно слово.")

        self.words = words

        pattern = r"\b(" + "|".join(map(re.escape, words)) + r")\b"
        self.regex = re.compile(
            pattern,
            flags=re.IGNORECASE | re.UNICODE,
        )

    def __call__(self, value):
        if not self.regex.search(value):
            raise ValidationError(
                self.message.format(words=", ".join(self.words)),
                code=self.code,
            )

    def __eq__(self, other):
        return (
            isinstance(other, ValidateMustContain)
            and self.words == other.words
        )
