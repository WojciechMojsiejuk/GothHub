from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden, HttpResponse
from home.forms import FileUploadForm
from home.models import File, Repository, Catalog


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
        if form.is_valid():
            dir = form.cleaned_data.get('dir')
            File.objects.create(
                author=user,
                file_name=dir,
                # extension=
                repository_Id=repo,
                catalog_Id=parental_catalog,
            )
            return HttpResponseRedirect("/")
            # redirect('upload_file')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})
