from django.urls import path, include
from logowanie import views as views_logowanie

from . import views


app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('user/<str:username>/add_repository', views.add_repository, name='add_repository'),
    path('user/<str:username>', views.user, name='user'),
    path('user/<str:username>/edit', views_logowanie.edit_profile, name='edit_profile'),
    path('statistics', include('repository_statistics.urls')),
    path('user/<str:username>/<str:repository>', views.repository, name='repository'),
    path('user/<str:username>/<str:repository>/delete_repository', views.delete_repository, name='delete_repository'),
    path('user/<str:username>/<str:repository>/<path:path>/upload', include('upload.urls')),
    path('user/<str:username>/<str:repository>/add_catalog', views.add_catalog, name='add_catalog'),
    path('user/<str:username>/<str:repository>/<path:path>/add_catalog', views.add_catalog, name='add_catalog'),
    path('user/<str:username>/<str:repository>/<path:path>/files/<str:filename>/<str:version>', views.show_file, name='show_file'),
    path('user/<str:username>/<str:repository>/<path:path>/delete_catalog', views.delete_catalog, name='delete_catalog'),
    path('user/<str:username>/<str:repository>/<path:path>', views.catalogs_and_files, name='catalogs_and_files')
]
