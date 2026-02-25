import re

import django.utils.deconstruct

WORDS_REGEX = re.compile(r"\w+|\W+")


@django.utils.deconstruct.deconstructible
class ValidateMustContain:
    message = "Текст должен содержать хотя бы одно из слов: {words}."
    code = "must_contain"

    def __init__(self, *words):
        if not words:
            raise ValueError("Необходимо передать хотя бы одно слово.")

        self.validate_wods = {word.lower() for word in words}
        self.joined_words = ", ".join(self.validate_wods)

    def __call__(self, value):
        words = set(WORDS_REGEX.findall(value.lower()))
        if not self.validate_wods & words:
            raise django.core.exceptions.ValidationError(
                f"В тексте `{value}` нет слов: {self.joined_words}",
            )
