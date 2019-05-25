from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


from .models import Repository
from .forms import RepoCreationForm,CatalogCreationForm

def home(request):
    if request.user.is_authenticated:
        user = request.user
        return HttpResponseRedirect('/' + user.username)
    else:
        return render(request, 'home.html', {})

def user(request, username):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    return render(request, 'users_profile.html', {'user':user})


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

def catalog(request, username, repository):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = CatalogCreationForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                searched_repository=Repository.objects.get(owner=user,name=repository)
                Catalog.objects.create(name=name,repository_Id=searched_repository.pk,parent_catalog=None)
                return HttpResponseRedirect('/')
            else:
                form = CatalogCreationForm()
                catalogs=Catalog.objects.filter(repository_Id=Repository.objects.get(owner=user,name=repository).pk)
            return render(request, 'catalog.html',{'form':form,'catalogs':catalogs})
    else:
        raise 404
