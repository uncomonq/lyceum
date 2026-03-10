from django import forms


class EchoForm(forms.Form):
    text = forms.CharField(
        label="Текст",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
            },
        ),
    )
