from django import forms
from .models import *


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


class SignUpForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = User
        widgets = {
            'username': forms.TextInput(),
            'password': forms.PasswordInput(),
        }
