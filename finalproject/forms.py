from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class SearchForm(forms.ModelForm):
    class Meta:
        widgets = {
            'param1': forms.TextInput(attrs={
                'name': 'param1',
                'placeholder': 'Search by genre, artist or event',
                'type': 'text',
                'aria-label': 'keywords',
                'class': 'form-control'

            }),
            'param2': forms.TextInput(attrs={
                'name': 'param2',
                'placeholder': 'Enter a city e.g., Hartford',
                'type': 'text',
                'aria-label': 'keywords',
                'class': 'form-control'
            }),
        }


class SignInForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = User
        widgets = {
            'username': forms.TextInput(),
            'password': forms.PasswordInput(),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')  # Customize the list of fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'custom-class'})
        self.fields['password1'].widget.attrs.update({'class': 'custom-class'})
        self.fields['password2'].widget.attrs.update({'class': 'custom-class'})
