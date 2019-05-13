from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Repository
from .forms import RepoCreationForm

def home(request):
    return render(request, 'home.html', {})

def repository(request):
    if request.method == 'POST':
        form = RepoCreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            is_public = form.cleaned_data.get('is_public')
            Repository.objects.create(name=name, is_public=is_public)
            return HttpResponseRedirect('/')
    else:
        form = RepoCreationForm()
        repositories = Repository.objects.all()
    return render(request, 'repository.html', {'form':form, 'repositories':repositories})
