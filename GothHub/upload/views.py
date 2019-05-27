from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404, HttpRequest
from django.conf import settings
import os

from home.models import File
from home.forms import FileForm

def file_list(request):
    files = Uploaded_file.objects.all()
    return render(request, 'download.html', {'files':files})

def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            dir = form.cleanded_data.get('dir')
            File.objects.create(
            author =
            file_name =
            extension =
            content =
            date_upload =
            repository_Id =
            catalog_Id =
            )
            return redirect('download')
    else:
        form = FileForm()
    return render(request, 'upload_file.html', {'form':form})
