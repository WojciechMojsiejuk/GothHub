from django.shortcuts import render

from .models import Repository
from .forms import RepoCreationForm

def home(request):
    return render(request, 'home.html', {})

def repository(request):
    if request.method == 'POST':
        repositories = RepoCreationForm(request.POST)
        name = repositories.cleaned_data.get('name')
        is_public = repositories.cleaned_data.get('is_public')
        repo = Repository(name=name, is_public=is_public)
        repo.save()
        return redirect('/')
    else:
        repositories = RepoCreationForm()
    repositories = Repository.objects.all()
    return render(request,'repository.html',{'repositories':repositories})
