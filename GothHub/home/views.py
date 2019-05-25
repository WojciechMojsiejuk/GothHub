from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


from .models import Repository
from .forms import RepoCreationForm,CatalogCreationForm

def home(request):
    logged_user = request.user
    if logged_user.is_authenticated is True:
        repositories = Repository.objects.filter(owner=logged_user)
        return render(request, 'home.html', {'repositories':repositories})
    return render(request, 'home.html', {'repositories':None})


def user(request, username):
    logged_user = request.user
    owner = User.objects.get(username=username)
    repositories_owner = Repository.objects.filter(owner=owner)
    if logged_user.is_authenticated is True:
        repositories = Repository.objects.filter(owner=logged_user)
        return render(request, 'users_profile.html', {'username':username, 'repositories':repositories,
            'repositories_owner':repositories_owner})
    return render(request, 'users_profile.html', {'username':username, 'repositories':None,
        'repositories_owner':repositories_owner})



def add_repository(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = RepoCreationForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                is_public = form.cleaned_data.get('is_public')
                Repository.objects.create(name=name, is_public=is_public, owner=user)
                return HttpResponseRedirect('/')
        else:
            form = RepoCreationForm()
            repositories = Repository.objects.filter(owner=user)
        return render(request, 'repository.html', {'form':form, 'repositories':repositories})
    else:
        return HttpResponseRedirect('/')

def repository(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = RepoCreationForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                is_public = form.cleaned_data.get('is_public')
                Repository.objects.create(name=name, is_public=is_public, owner=user)
                return HttpResponseRedirect('/')
        else:
            form = RepoCreationForm()
            repositories = Repository.objects.filter(owner=user)
        return render(request, 'repository.html', {'form':form, 'repositories':repositories})
    else:
        return HttpResponseRedirect('/')

def catalog(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = CatalogCreationForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
