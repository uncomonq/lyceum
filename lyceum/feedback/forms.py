from django import forms

from feedback.models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("name", "mail", "text")
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
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ваше имя"},
            ),
            "mail": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "name@example.com",
                },
            ),
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Текст обращения",
                },
            ),
        }
