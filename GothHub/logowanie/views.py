from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden

from home.models import Repository

from .models import Profile
from .forms import SignUpForm, LoginForm, EditUsernameForm, EditPasswordForm
from .tokens import account_activation_token


# Registering a user
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('logowanie/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return HttpResponse('Wysłano email z linkiem aktywacyjnym')
    else:
        form = SignUpForm()
    return render(request, 'logowanie/signup.html', {'form': form})


# Basic login view
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.profile.email_confirmed:
                    login(request, user)
                    return HttpResponseRedirect('/user/'+user.username)
                else:
                    return HttpResponse('Nie potwierdzono adresu email podanego użytkownika')
            else:
                form = LoginForm()
                return render(request, 'logowanie/signup.html', {
                    'form': form,
                    'error_message': 'Nie znaleziono użytkownika'
                })
        else:
            form = LoginForm()
            return render(request, 'logowanie/signup.html', {
                'form': form,
                'error_message': 'Nieprawidłowy login lub hasło'
            })
    else:
        form = LoginForm()
    return render(request, 'logowanie/signup.html', {'form': form})

# Users profile edition
# TO DO: CHECK FORMS
def edit_profile(request, username):
    if request.user.is_authenticated is True:
        logged_user = request.user
        if logged_user.username == username:
            repositories = Repository.objects.filter(owner=logged_user)
            if request.method == 'POST':
                username_form = EditUsernameForm(request.POST)
                password_form = EditPasswordForm(request.POST)
                if username_form.is_valid():
                    update_username = username_form.cleaned_data.get('username')
                    logged_user.username = update_username
                if password_form.is_valid():

                    update_password = form.cleaned_data.get('new_password')
                    logged_user.password = update_password
                logged_user.save()
                return HttpResponse('Zmieniono dane')
            else:
                username_form = EditUsernameForm()
                password_form = EditPasswordForm()
            return render(request, 'logowanie/edit_profile.html', {'username_form': username_form,
                'password_form': password_form, 'user': logged_user, 'repositories': repositories})
    return HttpResponseForbidden("Can only edit own profile")


# Checks if activation token is correct, validates email
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return HttpResponseRedirect('/')

    else:
        return HttpResponse('Nie zalogowano')


def pagelogout(request):
    if request.method == "POST":
        logout(request)
        return redirect('/')
