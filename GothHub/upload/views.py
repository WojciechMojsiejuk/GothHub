from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from home.forms import FileUploadForm
from home.models import File, Repository, Catalog
from django.http import HttpResponse
from repository_statistics.models import ProgrammingLanguage

import os

def upload_file(request, username, repository, parental_catalog, catalog):
    user = request.user
    repo = Repository.objects.get(owner=user, name=repository)
    if parental_catalog is not None:
        catalog = Catalog.objects.get(
            name=catalog,
            repository_Id=repo,
            parent_catalog=Catalog.objects.get(name=parental_catalog, repository_Id=repo))
    else:
        catalog = Catalog.objects.get(name=catalog, repository_Id=repo, parent_catalog=None)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            dir = form.cleaned_data.get('dir')
            ex = os.path.splitext(dir)[1]
            ex = ex.lstrip('.')
            allowed_extensions = str(ProgrammingLanguage.objects.all().values_list('extensions',flat=True)).split(',')
            if ex in allowed_extensions:
                File.objects.create(
                    author=user,
                    file_name=dir,
                    extension= ex,
                    repository_Id=repo,
                    catalog_Id=catalog,
                )

            try:
                older_files = File.objects.filter(file_name=dir, author=user, repository_Id=repo, catalog_Id=catalog
                latest_version = Version.objects.get(file_Id__in=older_files).latest('version_nr')
                Version.objects.create(
                file_Id = uploaded_file,
                version_nr = latest_version+1,
                )

            except File.DoesNotExist:
                older_files=None
                Version.objects.create(
                file_Id = uploaded_file,
                version_nr = 1,
                )
                return redirect('download')

            else:
                return HttpResponse('Bad extension', status = 406)
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})
