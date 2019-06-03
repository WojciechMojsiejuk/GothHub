from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from home.models import Repository, Catalog, File
from django.contrib.auth.decorators import login_required
from .models import ProgrammingLanguage

# Create your views here.
@login_required(login_url='/login/')
def show_statistics(request):
    user = request.user
    try:
        users_public_repositories = Repository.objects.filter(owner=user, is_public=True)
        users_public_repositories_count = users_public_repositories.count()
    except Repository.DoesNotExist:
        users_public_repositories_count = 0
    try:
        users_private_repositories = Repository.objects.filter(owner=user, is_public=False)
        users_private_repositories_count = users_private_repositories.count()
    except Repository.DoesNotExist:
        users_private_repositories_count = 0
    try:
        users_repositories = Repository.objects.filter(owner=user)
        users_catalogs_count = Catalog.objects.filter(repository_Id__in=users_repositories).count()
    except Catalog.DoesNotExist:
        users_catalogs_count = 0

    python_extensions_list = ProgrammingLanguage.objects.filter(name__exact='Python').values_list('extensions',
                                                                                                  flat=True)
    java_extensions_list = ProgrammingLanguage.objects.filter(name__exact='Java').values_list('extensions',
                                                                                                  flat=True)
    c_extensions_list = ProgrammingLanguage.objects.filter(name__exact='C').values_list('extensions',
                                                                                                  flat=True)
    cpp_extensions_list = ProgrammingLanguage.objects.filter(name__exact='C++').values_list('extensions',
                                                                                                  flat=True)
    chash_extensions_list = ProgrammingLanguage.objects.filter(name__exact='C#').values_list('extensions',
                                                                                               flat=True)
    other_extensions_list = ProgrammingLanguage.objects.filter(name__exact='Other').values_list('extensions',
                                                                                               flat=True)
    try:
        python_users_files_count = File.objects.filter(author=user, extension__in=python_extensions_list).count()
    except File.DoesNotExist:
        python_users_files_count = 0
    try:
        java_users_files_count = File.objects.filter(author=user, extension__in=java_extensions_list).count()
    except File.DoesNotExist:
        java_users_files_count = 0
    try:
        c_users_files_count = File.objects.filter(author=user, extension__in=c_extensions_list).count()
    except File.DoesNotExist:
        c_users_files_count = 0
    try:
        cpp_users_files_count = File.objects.filter(author=user, extension__in=cpp_extensions_list).count()
    except File.DoesNotExist:
        cpp_users_files_count = 0
    try:
        chash_users_files_count = File.objects.filter(author=user, extension__in=chash_extensions_list).count()
    except File.DoesNotExist:
        chash_users_files_count = 0
    try:
        other_users_files_count = File.objects.filter(author=user, extension__in=other_extensions_list).count()
    except File.DoesNotExist:
        other_users_files_count = 0

    return render(request, 'users_repositories_statistics.html',
                  {
                      'username': user,
                      'public_repositories': users_public_repositories_count,
                      'private_repositories': users_private_repositories_count,
                      'users_catalogs': users_catalogs_count,
                      'python_users_files_count': python_users_files_count,
                      'java_users_files_count': java_users_files_count,
                      'c_users_files_count': c_users_files_count,
                      'cpp_users_files_count': cpp_users_files_count,
                      'chash_users_files_count': chash_users_files_count,
                      'other_users_files_count': other_users_files_count
                  })
