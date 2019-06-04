from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from home.forms import FileUploadForm
from home.models import File, Repository, Catalog

import os

def upload_file(request, username, repository, parental_catalog, catalog):
    user = request.user
    repo = Repository.objects.get(owner=user, name=repository)
    if parental_catalog is None:
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
            File.objects.create(
                author=user,
                file_name=dir,
                extension= os.path.splitext(dir)[1],
                repository_Id=repo,
                catalog_Id=catalog,
            )
            return redirect('download')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})
