from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from .models import Repository, Catalog, File
from .forms import RepoCreationForm,CatalogCreationForm

def home(request):
    logged_user = request.user
    if logged_user.is_authenticated is True:
        repositories = Repository.objects.filter(owner=logged_user)
        for repository in repositories:
            print(repository)
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



def add_repository(request, username):
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
        return render(request, 'repository.html', {'form':form})
    else:
        return HttpResponseRedirect('/')

def repository(request, username, repository):
    if request.user.is_authenticated:
        user = request.user
        searched_repository=Repository.objects.get(owner=user,name=repository)
        try:
            catalogs=Catalog.objects.filter(repository_Id=searched_repository)
        except(Catalog.DoesNotExist):
            catalogs=None
        searched_parental_catalog=None
        try:
            files=File.objects.filter(author=user,repository_Id=searched_repository, catalog_Id=searched_parental_catalog)
        except(File.DoesNotExist):
            files=None
        return render(request, 'repository_catalogs_and_files.html', {'username':user, 'repository':searched_repository,'parent_catalog':searched_parental_catalog,'catalogs':catalogs,'files':files})
    else:
        return HttpResponseRedirect('/')

def add_catalog(request, username, repository, parental_catalog):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = CatalogCreationForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                searched_repository=Repository.objects.get(owner=user,name=repository)
                print(searched_repository.id)
                if parental_catalog == 'None':
                    Catalog.objects.create(name=name,repository_Id=searched_repository,parent_catalog=None)
                else:
                    searched_parental_catalog=Catalog.objects.get(name=parental_catalog,repository_Id=searched_repository)
                    Catalog.objects.create(name=name,repository_Id=searched_repository,parent_catalog=searched_parental_catalog)
                return HttpResponseRedirect('/')
        else:
            form = CatalogCreationForm()
        return render(request, 'catalog.html',{'form':form})
    else:
        raise 404

def catalogs_and_files(request,username,repository,parental_catalog):
    if request.user.is_authenticated:
        user = request.user
        searched_repository=Repository.objects.get(owner=user,name=repository)
        try:
            catalogs=Catalog.objects.filter(repository_Id=searched_repository)
        except(Catalog.DoesNotExist):
            catalogs=None
        try:
            searched_parental_catalog=Catalog.objects.get(name=parental_catalog,repository_Id=searched_repository)
        except(Catalog.DoesNotExist):
            searched_parental_catalog=None
        try:
            files=File.objects.filter(author=user,repository_Id=searched_repository, catalog_Id=searched_parental_catalog)
        except(File.DoesNotExist):
            files=None
        return render(request, 'repository_catalogs_and_files.html', {'username':user, 'repository':searched_repository,'parent_catalog':searched_parental_catalog,'catalogs':catalogs,'files':files})
    else:
        return HttpResponseRedirect('/')

def delete_catalog_and_files_within_it(request,username,repository,parental_catalog,catalog):
    if request.user.is_authenticated:
        user = request.user
        searched_repository=Repository.objects.get(owner=user,name=repository)
        try:
            searched_parental_catalog=Catalog.objects.get(name=parental_catalog,repository_Id=searched_repository)
        except(Catalog.DoesNotExist):
            searched_parental_catalog=None
        try:
            searched_catalog = Catalog.objects.get(name=catalog,repository_Id=searched_repository,parent_catalog=searched_parental_catalog)
        except(Catalog.DoesNotExist):
            raise 404
        try:
            files_in_searched_catalog = File.objects.filter(author=user,repository_Id=searched_repository,catalog_Id = searched_catalog)
            files_in_searched_catalog.delete()
        except(File.DoesNotExist):
            pass
        searched_catalog.delete()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
