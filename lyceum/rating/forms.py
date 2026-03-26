from django import forms
import rating.models


class RatingForm(forms.ModelForm):
    class Meta:
        model = rating.models.Rating
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["value"].required = False
        self.fields["value"].choices = [
            ("", "Без оценки"),
            *rating.models.Rating.Value.choices,
        ]
