from django.shortcuts import render
from home.models import Repository
def home(request):
    return render(request, 'home.html', {})

def repository(request):
    if request.method == 'POST':
        Repository.objects.create(name=request.POST.cleaned_data.get('name'),is_public=request.POST.cleaned_data.get('is_public'))
        return redirect('/')
    repositories = Repository.objects.all()
    return render(request,'repository.html',{'repositories':repositories})
