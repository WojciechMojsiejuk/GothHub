from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    login = False
    email = forms.EmailField(max_length=254, help_text='\n Wymagany. Podaj prawidłowy adres email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username' : 'Nazwa użytkownika',
        }

class LoginForm(AuthenticationForm):
    login = True

    class Meta:
        model = User
        fields = ('username', 'password')

class EditUsernameForm(forms.Form):
    username = forms.CharField(max_length=128, label="Nazwa użytkownika")

    class Meta:
        model = User


class EditPasswordForm(forms.Form):
    password = forms.CharField(label="Hasło",
        widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Nowe hasło",
        widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Powtórz nowe hasło",
        widget=forms.PasswordInput)

    class Meta:
        model = User

    def clean(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            msg = "Podane hasła nie są takie same"
            self.add_error('new_password2', msg)
