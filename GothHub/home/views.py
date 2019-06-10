from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden, HttpResponse, HttpResponseServerError, \
    HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Repository, Catalog, File, Version
from .forms import RepoCreationForm, CatalogCreationForm, ShowFileForm
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


def home(request):
    return render(request, 'home.html', {})


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
                try:
                    Repository.objects.get(name=name, owner=user)
                    form.add_error('name', "Repozytorium o takiej nazwie już istnieje")
                except Repository.DoesNotExist:
                    Repository.objects.create(name=name, is_public=is_public, owner=user)
                    repositories = Repository.objects.filter(owner=user)
                    request.session['repositories'] = [repository.name for repository in repositories]
                    return HttpResponseRedirect('/')
        else:
            form = RepoCreationForm()
        return render(request, 'repository.html', {'form': form})
    else:
        return HttpResponseForbidden('You are not authorized to add repository')


@login_required
def edit_repository(request, username, repository):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    if request.user == user:
        try:
            changed_repository = Repository.objects.get(name=repository, owner=user)
        except Repository.DoesNotExist:
            raise Http404("Repository does not exist")
        if request.method == 'POST':
            form = RepoCreationForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                is_public = form.cleaned_data.get('is_public')
                changed_repository.name = name
                changed_repository.is_public = is_public
                changed_repository.save()
                repositories = Repository.objects.filter(owner=user)
                request.session['repositories'] = [repository.name for repository in repositories]
                return HttpResponseRedirect('/user/' + username)
        else:
            form = RepoCreationForm(initial={'name' : changed_repository.name , 'is_public' : changed_repository.is_public})
        return render(request, 'repository.html', {'form': form})
    else:
        return HttpResponseForbidden('You are not authorized to edit repository')


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
    return render(request, 'repository_catalogs_and_files.html',
                  {
                      'username': user,
                      'repository': searched_repository,
                      'path': "/user/" + user.username + '/' + searched_repository.name,
                      'catalogs': catalogs
                  })


@login_required
def delete_repository(request, username, repository):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")

    if request.user == user:
        try:
            searched_repository = Repository.objects.get(owner=user, name=repository)
            searched_repository.delete()
            repositories = Repository.objects.filter(owner=user)
            request.session['repositories'] = [repository.name for repository in repositories]
        except Repository.DoesNotExist:
            raise Http404("Repository does not exists")
        return HttpResponseRedirect('/user/' + user.username)
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
            catalogs_path = path.split('/')
            for n, catalog in enumerate(catalogs_path):
                if n == 0:
                    try:
                        parental_catalog = Catalog.objects.get(name=catalog, repository_Id=searched_repository,
                                                               parent_catalog=None)
                    except Catalog.DoesNotExist:
                        raise Http404("Catalog does not exist")
                else:
                    try:
                        parental_catalog = Catalog.objects.get(name=catalog, repository_Id=searched_repository,
                                                               parent_catalog=parental_catalog)
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
    else:
        try:
            searched_repository = Repository.objects.get(owner=user, name=repository, is_public=True)
        except Repository.DoesNotExist:
            raise Http404("Repository does not exist")
    if path is not None:
        catalogs_path = path.split('/')
        urls = []
        url = '/user/' + user.username + '/' + searched_repository.name
        for n, catalog in enumerate(catalogs_path):
            if n == 0:
                try:
                    parental_catalog = Catalog.objects.get(name=catalog, repository_Id=searched_repository,
                                                           parent_catalog=None)
                except Catalog.DoesNotExist:
                    raise Http404("Catalog does not exist")
            else:
                try:
                    parental_catalog = Catalog.objects.get(name=catalog, repository_Id=searched_repository,
                                                           parent_catalog=parental_catalog)
                except Catalog.DoesNotExist:
                    raise Http404("Catalog does not exist")
            url = url + '/' + catalog
            urls.append((catalog, url))
    try:
        catalogs = Catalog.objects.filter(repository_Id=searched_repository, parent_catalog=parental_catalog)
    except Catalog.DoesNotExist:
        catalogs = None
    try:
        files = File.objects.filter(author=user, repository_Id=searched_repository,
                                    catalog_Id=parental_catalog).values('file_name').distinct()
    except File.DoesNotExist:
        files = None
    path = '/user/' + user.username + '/' + searched_repository.name + '/' + path
    return render(request, 'repository_catalogs_and_files.html', {
        'username': user.username,
        'repository': searched_repository,
        'catalogs_path': urls,
        'path': path,
        'catalogs': catalogs,
        'files': files
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
                        parental_catalog = Catalog.objects.get(name=catalog, repository_Id=searched_repository,
                                                               parent_catalog=None)
                    except Catalog.DoesNotExist:
                        raise Http404("Catalog does not exist")
                else:
                    try:
                        parental_catalog = Catalog.objects.get(name=catalog, repository_Id=searched_repository,
                                                               parent_catalog=parental_catalog)
                    except Catalog.DoesNotExist:
                        raise Http404("Catalog does not exist")
        else:
            raise Http404("Catalog does not exist")

        parental_catalog.delete()
        if len(catalogs_path) != 1:
            new_path = '/user/' + username + '/' + searched_repository.name + '/' + path[:-(len(catalogs_path[-1])+1)]
            return HttpResponseRedirect(new_path)
        else:
            new_path = '/user/' + username + '/' + searched_repository.name
            return HttpResponseRedirect(new_path)
    else:
        return HttpResponse('Unauthorized', status=401)


@login_required
def edit_catalog(request, username, repository, path):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    if request.user == user:
        try:
            searched_repository = Repository.objects.get(name=repository, owner=user)
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
        if request.method == 'POST':
            form = CatalogCreationForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                parental_catalog.name = name
                parental_catalog.save()
                if len(catalogs_path) != 1:
                    new_path = '/user/' + username + '/' + searched_repository.name + '/' + path[:-(len(catalogs_path[-1])+1)]
                    return HttpResponseRedirect(new_path)
                else:
                    new_path = '/user/' + username + '/' + searched_repository.name
                    return HttpResponseRedirect(new_path)
        else:
            form = CatalogCreationForm(initial={'name' : parental_catalog.name})
        return render(request, 'catalog.html', {'form': form})
    else:
        return HttpResponseForbidden('You are not authorized to edit catalog')


@login_required
def show_file(request, username, repository, path, filename, version):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    try:
        searched_repository = Repository.objects.get(owner=user, name=repository)
    except Repository.DoesNotExist:
        raise Http404("Repository does not exist")
    if request.user == user or (request.user != user and searched_repository.is_public is True):
        if path is not None:
            if request.method == 'POST':
                form = ShowFileForm(request.POST)
                if form.is_valid():
                    version = form.cleaned_data.get('version_nr')
                    print("WERSJA")
                    print(version)

            else:
                ShowFileForm()
                catalogs_path = path.split('/')
                for n, catalog in enumerate(catalogs_path):
                    if n == 0:
                        try:
                            parental_catalog = Catalog.objects.get(name=catalog, repository_Id=searched_repository,
                                                                   parent_catalog=None)
                        except Catalog.DoesNotExist:
                            raise Http404("Catalog does not exist")
                    else:
                        try:
                            parental_catalog = Catalog.objects.get(name=catalog, repository_Id=searched_repository,
                                                                   parent_catalog=parental_catalog)
                        except Catalog.DoesNotExist:
                            raise Http404("Catalog does not exist")
                # TODO: make function from the above (this code is repeated many times)
                # Get file:
                try:
                    matching_files = File.objects.filter(
                        file_name=filename,
                        author=user,
                        repository_Id=searched_repository,
                        catalog_Id=parental_catalog)
                    print(matching_files)
                except File.DoesNotExist:
                    raise Http404("File does not exists")
                if version == "latest":
                    try:
                        selected_file = Version.objects.filter(file_Id__in=matching_files).latest('version_nr')
                        print(selected_file)
                    except Version.DoesNotExist:
                        return HttpResponseServerError("Versioning error")
                else:
                    try:
                        selected_file = Version.objects.get(file_Id__in=matching_files, version_nr=int(version))
                    except ValueError:
                        HttpResponseBadRequest("Invalid version number")
                    except Version.DoesNotExist:
                        return Http404("Version does not exist")

                f = open('media/' + str(selected_file.file_Id.dir), 'r')
                file_content = f.read()
                print(file_content)
                f.close()
                context = {'file_content': file_content,
                           'versions': Version.objects.filter(file_Id__in=matching_files),
                           'username': user,
                           'repository': searched_repository,
                           'path': path}
                return render(request, "file.html", context, content_type="text/html")
            return
        else:
            raise Http404("Catalog does not exist")
    else:
        return HttpResponse('Unauthorized', status=401)


@login_required
def compare_files(request, username, repository, path, filename, version1, version2):
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
                        parental_catalog = Catalog.objects.get(name=catalog, repository_Id=searched_repository,
                                                               parent_catalog=None)
                    except Catalog.DoesNotExist:
                        raise Http404("Catalog does not exist")
                else:
                    try:
                        parental_catalog = Catalog.objects.get(name=catalog, repository_Id=searched_repository,
                                                               parent_catalog=parental_catalog)
                    except Catalog.DoesNotExist:
                        raise Http404("Catalog does not exist")
            # Get files:
            try:
                matching_files = File.objects.filter(
                    file_name=filename,
                    author=user,
                    repository_Id=searched_repository,
                    catalog_Id=parental_catalog)
                print(matching_files)
            except File.DoesNotExist:
                raise Http404("File does not exists")

            # FILE 1
            try:
                selected_file_1 = Version.objects.get(file_Id__in=matching_files, version_nr=int(version1))
            except ValueError:
                HttpResponseBadRequest("Invalid version number")
            except Version.DoesNotExist:
                return Http404("Version does not exist")

            # FILE 2
            try:
                selected_file_2 = Version.objects.get(file_Id__in=matching_files, version_nr=int(version2))
            except ValueError:
                HttpResponseBadRequest("Invalid version number")
            except Version.DoesNotExist:
                return Http404("Version does not exist")

            f = open('media/'+str(selected_file_1.file_Id.dir), 'r')
            file_1_content = f.read()
            f.close()
            f = open('media/'+str(selected_file_2.file_Id.dir), 'r')
            file_2_content = f.read()
            f.close()
            context = {'file_1_content': file_1_content,
                       'file_2_content': file_2_content,
                       'versions': Version.objects.filter(file_Id__in=matching_files),
                       'username': user,
                       'repository': searched_repository,
                       'path': path}
            return render(request, "files_comparison.html", context, content_type="text/html")
        else:
            raise Http404("Catalog does not exist")
    else:
        return HttpResponse('Unauthorized', status=401)
