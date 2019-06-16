from django import forms
from django.contrib.auth.models import User
from .models import Keywords
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _, ngettext

#nadpisana na standardowej klasie django klasa rejestracji użytkownika
class NewUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label=_("Hasło"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Potwierdź hasło"),
                                widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

        labels = {
            'username': 'Nazwa użytkownika',
            'password1': 'Hasło',
            'password2': 'Potwierdź hasło',
            'email': 'Adres mailowy',
        }
        help_texts = {
            'username':  "",
            'password1': None,
            'password2': None,
        }

#aktualizacja danych użytkownika
class UpdateUser(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]
        labels = {
            'username': 'nazwa użytkownika',
            'email': 'adres mailowy',
        }

        help_texts = {'username': 'nazwa użytkownika musi być unikatowa'}

class NewKeyword(forms.ModelForm):
    class Meta:
        model = Keywords
        fields = ['name']

        labels = {'name':''}










