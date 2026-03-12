__all__ = ()
from django import forms

from feedback.models import Feedback, FeedbackPersonData


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if not data:
            return []

        if isinstance(data, (list, tuple)):
            return [
                single_file_clean(file_data, initial) for file_data in data
            ]

        return [single_file_clean(data, initial)]


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
        exclude = (
            "created_on",
            "status",
        )
        labels = {
            "text": "Текст обращения",
        }
        help_texts = {
            "text": "Введите текст обращения.",
        }
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Текст обращения",
                },
            ),
        }


class FeedbackAuthorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].required = False

        for field in self.visible_fields():
            css_classes = field.field.widget.attrs.get("class", "")
            field.field.widget.attrs["class"] = (
                f"{css_classes} form-control".strip()
            )

    class Meta:
        model = FeedbackPersonData
        exclude = ("feedback",)
        labels = {
            "name": "Имя",
            "mail": "Почта",
        }
        help_texts = {
            "name": "Укажите ваше имя.",
            "mail": "Укажите почту для обратной связи.",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ваше имя"}),
            "mail": forms.EmailInput(
                attrs={
                    "placeholder": "name@example.com",
                },
            ),
        }


class FeedbackFilesForm(forms.Form):
    files = MultipleFileField(
        label="Файлы",
        required=False,
        widget=MultipleFileInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            css_classes = field.field.widget.attrs.get("class", "")
            field.field.widget.attrs["class"] = (
                f"{css_classes} form-control".strip()
            )
