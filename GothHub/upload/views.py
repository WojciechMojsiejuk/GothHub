from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden, HttpResponse
from home.forms import FileUploadForm
from home.models import File, Repository, Catalog, Version
from django.http import HttpResponse
from repository_statistics.models import ProgrammingLanguage
from django.core.exceptions import MultipleObjectsReturned

import os


def upload_file(request, username, repository, path):
    user = request.user
    repo = Repository.objects.get(owner=user, name=repository)
    catalogs_path = path.split('/')
    for n, catalog in enumerate(catalogs_path):
        if n == 0:
            try:
                parental_catalog = Catalog.objects.get(name=catalog, repository_Id=repo, parent_catalog=None)
            except Catalog.DoesNotExist:
                raise Http404("Catalog does not exist")
        else:
            try:
                parental_catalog = Catalog.objects.get(name=catalog, repository_Id=repo, parent_catalog=parental_catalog)
            except Catalog.DoesNotExist:
                raise Http404("Catalog does not exist")
    # if parental_catalog is None:
    #     catalog = Catalog.objects.get(
    #         name=catalog,
    #         repository_Id=repo,
    #         parent_catalog=Catalog.objects.get(name=parental_catalog, repository_Id=repo))
    # else:
    #     catalog = Catalog.objects.get(name=catalog, repository_Id=repo, parent_catalog=None)
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(upladed_file.name, uploaded_file)

        if form.is_valid():
            #dir = form.cleaned_data.get('dir')
            ex = os.path.splitext(str(name))[1]
            ex = ex.lstrip('.')
            allowed_extensions_list = list(ProgrammingLanguage.objects.all().values_list('extensions', flat=True))
            allowed_extensions = []
            for i in allowed_extensions_list:
                allowed_extensions.extend(str(i).split(','))
            print(ex)
            print(allowed_extensions)
            if ex in allowed_extensions:
                print('kurea')
                uploaded_file = File.objects.create(
                    author=user,
                    file_name=name,
                    extension=ex,
                    repository_Id=repo,
                    catalog_Id=parental_catalog,
                )

                try:
                    previous_file = File.objects.get(file_name=dir, author=user, repository_Id=repo, catalog_Id=parental_catalog)
                    latest_version = Version.objects.get(file_Id=previous_file).values('version_nr')
                    Version.objects.create(
                        file_Id=uploaded_file,
                        version_nr=latest_version['version_nr'] + 1,
                    )

                except File.DoesNotExist:
                    Version.objects.create(
                        file_Id=uploaded_file,
                        version_nr=1,
                    )
                    return HttpResponse('gut')
                except MultipleObjectsReturned:
                    try:
                        older_files = File.objects.filter(file_name=dir, author=user, repository_Id=repo, catalog_Id=parental_catalog)
                        latest_version = Version.objects.get(file_Id=older_files).values('version_nr').latest('version_nr')
                        Version.objects.create(
                            file_Id=uploaded_file,
                            version_nr=latest_version['version_nr'] + 1,
                        )
                    except File.DoesNotExist:
                        return HttpResponse('Internal Server Error', status=500)
            else:
                return HttpResponse('Bad extension', status=406)
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})
