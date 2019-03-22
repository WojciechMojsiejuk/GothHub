from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User


from .forms import SignUpForm, LoginForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('login:index')
    else:
        form = SignUpForm()
    return render(request, 'logowanie/signup.html', {'form': form})

def index(request):
    if request.user.is_authenticated:
        # user home page needed
        return HttpResponseRedirect('/admin/')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('Zalogowano poprawnie')
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
