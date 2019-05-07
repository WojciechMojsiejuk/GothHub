from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Repository
from .forms import RepoCreationForm

def home(request):
    return render(request, 'home.html', {})

def repository(request):
    if request.method == 'POST':
        repositories = RepoCreationForm(request.POST)
        if repositories.is_valid():
            repo = repositories.save(commit=True)
            # repo.name = repositories.cleaned_data.get('name')
            # repo.is_public = repositories.cleaned_data.get('is_public')
            # repo.save()
            # Repository.objects.create(name=name, is_public=is_public)
            return redirect('/')
    else:
        repositories = RepoCreationForm()
    return render(request,'repository.html',{'repositories':repositories})
