from django import forms
from .models import ReviewModel


class CommentForm(forms.ModelForm):
    RATINGS_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    ratings = forms.ChoiceField(
        choices=RATINGS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = ReviewModel
        fields = ['ratings', 'comment']
