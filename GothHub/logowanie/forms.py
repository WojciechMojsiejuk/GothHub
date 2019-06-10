from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User

from captcha.fields import CaptchaField

class SignUpForm(UserCreationForm):
    login = False
    email = forms.EmailField(max_length=254, help_text='\n Wymagany. Podaj prawidłowy adres email')
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username' : 'Nazwa użytkownika',
        }
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Podaj nazwę składającą się jedynie z liter, cyfr i @, ., +, -, _'
        self.fields['email'].help_text = 'Podaj adres e-mail'
        self.fields['password1'].help_text = 'Podaj hasło składające się z min. 8 znaków - liter i cyfr'
        self.fields['password2'].help_text = 'Powtórz hasło'


class LoginForm(AuthenticationForm):
    login = True

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Nazwa użytkownika'


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
        # help_texts = {
        #     'password': 'Wpisz dotychczasowe hasło, aby potwierdzić swoją tożsamość',
        #     'new_password1': 'Nowe musi spełniać następujące warunki:
        #     Twoje hasło nie może być zbyt podobne do twoich innych danych osobistych.
        #     Twoje hasło musi zawierać co najmniej 8 znaków.
        #     Twoje hasło nie może być powszechnie używanym hasłem.
        #     Twoje hasło nie może składać się tylko z cyfr.'
        # }

    def clean(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            msg = "Podane hasła nie są takie same"
            self.add_error('new_password2', msg)
