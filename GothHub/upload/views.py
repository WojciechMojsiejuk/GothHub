from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404, HttpRequest
from django.conf import settings
import os

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    #print(file_path)
    #print(path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read())
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
