from django import forms
from .models import Score


class ScoreModelForm(forms.ModelForm):
    value = forms.IntegerField(min_value=0, max_value=10)

    class Meta:
        model = Score
        fields = [
            'value', 'content',
        ]
