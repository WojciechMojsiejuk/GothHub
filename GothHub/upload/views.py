from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from home.forms import FileUploadForm
from home.models import File, Repository, Catalog
#from datetime import datetime

'''
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)
'''

def upload_file(request, username, repository, parental_catalog, catalog):
    #parsed = urllib.parse.urlparse(request.build_absolute_uri())
    #print(parsed.path)
    user = request.user
    repo = Repository.objects.get(owner = user, name = repository)
    if parental_catalog == None:
        catalog = Catalog.objects.get(
        name = catalog,
        repository_Id = repo,
        parent_catalog = Catalog.objects.get(name = parental_catalog, repository_Id = repo, parent_catalog = null))
    else:
        catalog = Catalog.objects.get(name = catalog, repository_Id = repo, parent_catalog = null)
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            dir = form.cleaned_data.get('dir')
            #date = str(datetime.datetime.now().date()) + ' ' + str(datetime.datetime.now().time())
            #print(date)
            print(user)
            #print(dir)
            print(repository)
            #print(catalog_Id)
            File.objects.create(
            author = user,
            file_name = dir,
            #extension =
            #content =
            #date_upload = datetime.strptime(mydate, "%Y-%m-%d"),
            repository_Id = repo,
            catalog_Id = catalog,
            )
            return redirect('download')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form':form})
