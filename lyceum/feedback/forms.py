__all__ = ()
from django import forms

from feedback.models import Feedback


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            css_classes = field.field.widget.attrs.get("class", "")
            field.field.widget.attrs["class"] = (
                f"{css_classes} form-control".strip()
            )

    class Meta:
        model = Feedback
        exclude = ("created_on",)
        labels = {
            "name": "Имя",
            "mail": "Почта",
            "text": "Текст обращения",
        }
        help_texts = {
            "name": "Укажите ваше имя.",
            "mail": "Укажите почту для обратной связи.",
            "text": "Введите текст обращения.",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ваше имя"}),
            "mail": forms.EmailInput(
                attrs={
                    "placeholder": "name@example.com",
                },
            ),
            "text": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Текст обращения",
                },
            ),
        }
