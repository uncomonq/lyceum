__all__ = ()
from django import forms
from django.utils.translation import gettext_lazy as _

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
            "text": _("Message"),
        }
        help_texts = {
            "text": _("Enter the message text."),
        }
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": _("Message"),
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
            "name": _("Name"),
            "mail": _("Email"),
        }
        help_texts = {
            "name": _("Enter your name."),
            "mail": _("Enter your email address."),
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": _("Your name")}),
            "mail": forms.EmailInput(
                attrs={
                    "placeholder": "name@example.com",
                },
            ),
        }


class FeedbackFilesForm(forms.Form):
    files = MultipleFileField(
        label=_("Files"),
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
