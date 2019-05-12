from django.shortcuts import render

def upload(request):
#    if request.method == 'POST':
#        uploaded_file = request.FILES['']
    return render(request, 'upload.html', {})
