from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Komentarz, Ocena, Profil

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

class LoginForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

class KomentarzForm(forms.ModelForm):
    class Meta:
        model = Komentarz
        fields = ['tresc']
        widgets = {
            'tresc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dodaj komentarz...'})
        }

class OcenaForm(forms.ModelForm):
    class Meta:
        model = Ocena
        fields = ['ocena']
        widgets = {
            'ocena': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10})
        }