from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserAccount
from .constants import GENDER_TYPE


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'required'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'required'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'required'}))
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)

    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password",
        help_text=""
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirm Password",
        help_text=""
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'birth_date', 'gender']
        help_texts = {
            'username': None
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit == True:
            user.save()
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')

            UserAccount.objects.create(
                author=user,
                gender=gender,
                birth_date=birth_date,
            )
        return user
