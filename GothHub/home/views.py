from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User


from .models import Repository, Catalog
from .forms import RepoCreationForm, CatalogCreationForm

def home(request):
    if request.user.is_authenticated is True:
        logged_user = request.user
        repositories = Repository.objects.filter(owner=logged_user)
        return render(request, 'home.html', {'repositories':repositories})
    return render(request, 'home.html', {'repositories':None})


def user(request, username):
    try:
        owner = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    repositories = None
    repositories_owner = Repository.objects.filter(owner=owner, is_public=True)
    if request.user.is_authenticated is True:
        logged_user = request.user
        repositories = Repository.objects.filter(owner=logged_user)
        if logged_user == owner:
            repositories_owner = Repository.objects.filter(owner=owner)
    return render(request, 'users_profile.html', {'username':username, 'repositories':repositories,
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

def remove_repository(request, username, repository):
    if request.user.is_authenticated:
        user = request.user

    return HttpResponseRedirect('/')


def add_catalog(request, username, repository):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = CatalogCreationForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                searched_repository=Repository.objects.get(owner=user,name=repository)
                print(searched_repository.id)
                Catalog.objects.create(name=name,repository_Id=searched_repository,parent_catalog=None)
                return HttpResponseRedirect('/')
        else:
            form = CatalogCreationForm()
            catalogs=Catalog.objects.filter(repository_Id=Repository.objects.get(owner=user,name=repository).pk)
        return render(request, 'catalog.html',{'form':form,'catalogs':catalogs})
    else:
        raise 404
