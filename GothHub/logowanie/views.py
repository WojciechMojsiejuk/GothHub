from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import SignUpForm

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
    return HttpResponse("tu bedzie strona logowania")
