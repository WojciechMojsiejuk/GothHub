from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Repository, Catalog, File
from .forms import RepoCreationForm, CatalogCreationForm
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    if request.user.is_authenticated is True:
        logged_user = request.user
        repositories = Repository.objects.filter(owner=logged_user)
        return render(request, 'home.html', {'repositories': repositories})
    return render(request, 'home.html', {'repositories': None})


def user(request, username):
    try:
        owner = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    repositories_owner = Repository.objects.filter(owner=owner, is_public=True)
    if request.user.is_authenticated is True:
        logged_user = request.user
        if logged_user == owner:
            repositories_owner = Repository.objects.filter(owner=owner)
    return render(request, 'users_profile.html', {'username': username,
                                                  'repositories_owner': repositories_owner})

@login_required
def add_repository(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    if request.user == user:
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
        return render(request, 'repository.html', {'form': form})
    else:
        return HttpResponseForbidden('You are not authorized to add repository')

def repository(request, username, repository):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    if request.user == user:
        try:
            searched_repository = Repository.objects.get(owner=user, name=repository)
        except Repository.DoesNotExist:
            raise Http404("Repository does not exist")
    else:
        try:
            searched_repository = Repository.objects.get(owner=user, name=repository, is_public=True)
        except Repository.DoesNotExist:
            raise Http404("Repository does not exist or is not public")

    try:
        catalogs = Catalog.objects.filter(repository_Id=searched_repository, parent_catalog=None)
    except Catalog.DoesNotExist:
        catalogs = None
    searched_parental_catalog = None
    try:
        files = File.objects.filter(
            author=user,
            repository_Id=searched_repository,
            catalog_Id=searched_parental_catalog
        )
    except File.DoesNotExist:
        files = None
    return render(request, 'repository_catalogs_and_files.html',
                  {
                      'username': user,
                      'repository': searched_repository,
                      'parent_catalog': searched_parental_catalog,
                      'catalogs': catalogs, 'files': files
                  })

@login_required
def delete_repository(request, username, repository):
    # TODO: check other users permissions
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")

    if request.user == user:
        searched_repository = Repository.objects.get(owner=user, name=repository)
        searched_repository.delete()
        return HttpResponseRedirect('/')
    return HttpResponseForbidden('You are not authorized to delete this repository')

@login_required
def add_catalog(request, username, repository, path=None):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    if request.user == user:
        searched_repository = Repository.objects.get(owner=user, name=repository)
        if path is not None:
            print("elo")
            catalogs_path = path.split('/')
            for n, catalog in enumerate(catalogs_path):
                if n == 0:
                    try:
                        parental_catalog = Catalog.objects.get(name=catalog, repository_Id=searched_repository, parent_catalog=None)
                    except Catalog.DoesNotExist:
                        raise Http404("Catalog does not exist")
                else:
                    try:
                        Catalog.objects.get(name=catalog, repository_Id=searched_repository, parent_catalog=parental_catalog)
                    except Catalog.DoesNotExist:
                        raise Http404("Catalog does not exist")
        if request.method == 'POST':
            form = CatalogCreationForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                try:
                    Catalog.objects.get(name=name, repository_Id=searched_repository)
                    return render(request, 'catalog.html', {
                        'form': form,
                        'error_message': 'Nie można dodać katalogu o takiej nazwie, istnieje już w danej przestrzeni'
                    })
                except Catalog.DoesNotExist:
                    pass
                if path == None:
                    Catalog.objects.create(name=name, repository_Id=searched_repository, parent_catalog=None)
                    return HttpResponseRedirect('/user/' + str(user) + "/" + str(searched_repository.name))
                else:
                    Catalog.objects.create(
                        name=name,
                        repository_Id=searched_repository,
                        parent_catalog=parental_catalog
                    )
                    return HttpResponseRedirect('/user/' + str(user) + "/" + str(searched_repository.name) + "/" + path)
        else:
            form = CatalogCreationForm()
        return render(request, 'catalog.html', {'form': form})
    else:
        return HttpResponseForbidden('You are not authorized to add catalog')


def catalogs_and_files(request, username, repository, path):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    if request.user == user:
        try:
            searched_repository = Repository.objects.get(owner=user, name=repository)
        except Repository.DoesNotExist:
            raise Http404("Repository does not exist")
    try:
        searched_repository = Repository.objects.get(owner=user, name=repository, is_public=True)
    except Repository.DoesNotExist:
        raise Http404("Repository does not exist")
    if path is not None:
        catalogs_path = path.split('/')
        for n, catalog in enumerate(catalogs_path):
            if n == 0:
                try:
                    parental_catalog = Catalog.objects.get(name=catalog, repository_Id=searched_repository, parent_catalog=None)
                except Catalog.DoesNotExist:
                    raise Http404("Catalog does not exist")
            else:
                try:
                    parental_catalog = Catalog.objects.get(name=catalog, repository_Id=searched_repository, parent_catalog=parental_catalog)
                except Catalog.DoesNotExist:
                    raise Http404("Catalog does not exist")
    try:
        catalogs = Catalog.objects.filter(repository_Id=searched_repository, parent_catalog=parental_catalog)
    except Catalog.DoesNotExist:
        catalogs = None
    try:
        files = File.objects.filter(author=user, repository_Id=searched_repository,
                                    catalog_Id=parental_catalog)
    except File.DoesNotExist:
        files = None
    return render(request, 'repository_catalogs_and_files.html', {
        'user': user.username,
        'repository': searched_repository,
        'catalogs_path': catalogs_path,
        'catalogs': catalogs, 'files': files
    })

@login_required
def delete_catalog(request, username, repository, path):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    if request.user == user:
        try:
            searched_repository = Repository.objects.get(owner=user, name=repository)
        except Repository.DoesNotExist:
            raise Http404("Repository does not exist")
        if path is not None:
            catalogs_path = path.split('/')
            for n, catalog in enumerate(catalogs_path):
                if n == 0:
                    try:
                        parental_catalog = Catalog.objects.get(name=catalog, repository_Id=searched_repository, parent_catalog=None)
                    except Catalog.DoesNotExist:
                        raise Http404("Catalog does not exist")
                else:
                    try:
                        parental_catalog = Catalog.objects.get(name=catalog, repository_Id=searched_repository, parent_catalog=parental_catalog)
                    except Catalog.DoesNotExist:
                        raise Http404("Catalog does not exist")
        else:
            raise Http404("Catalog does not exist")

        parental_catalog.delete()
        return HttpResponseRedirect(
            '/user/' + str(user) + "/" + str(searched_repository.name) + "/" + path[:-(len(catalogs_path[-1])+1)])
    else:
        return HttpResponse('Unauthorized', status=401)
