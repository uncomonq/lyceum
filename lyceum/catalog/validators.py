__all__ = ("ValidateMustContain",)
import re

import django.core.exceptions
import django.utils.deconstruct
from django.utils.html import strip_tags

WORDS_REGEX = re.compile(r"\b[\w']+\b", flags=re.UNICODE)


@django.utils.deconstruct.deconstructible
class ValidateMustContain:
    message = "Текст должен содержать хотя бы одно из слов: {words}."
    code = "must_contain"

    def __init__(self, *words):
        if not words:
            raise ValueError("Необходимо передать хотя бы одно слово.")

        self.required_words = {word.lower() for word in words}
        self.joined_words = ", ".join(self.required_words)

    def __call__(self, value):
        plain_value = strip_tags(value)
        words = set(WORDS_REGEX.findall(plain_value.lower()))

        if not self.required_words & words:
            raise django.core.exceptions.ValidationError(
                f"В тексте `{value}` нет слов: {self.joined_words}",
            )
