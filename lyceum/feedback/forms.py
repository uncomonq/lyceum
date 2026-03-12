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
    name = forms.CharField(
        label="Имя",
        help_text="Укажите ваше имя.",
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Ваше имя"}),
    )
    mail = forms.EmailField(
        label="Почта",
        help_text="Укажите почту для обратной связи.",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "name@example.com",
            },
        ),
    )
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

    def save(self, commit=True):
        person = FeedbackPersonData.objects.create(
            name=self.cleaned_data["name"],
            mail=self.cleaned_data["mail"],
        )

        feedback_obj = super().save(commit=False)
        feedback_obj.person = person

        if commit:
            feedback_obj.save()

        return feedback_obj

    class Meta:
        model = Feedback
        fields = ("text",)
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
