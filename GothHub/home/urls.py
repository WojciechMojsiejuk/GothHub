from django.urls import path

from logowanie import views as views_logowanie

from . import views


app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('user/<str:username>/add_repository', views.add_repository, name='add_repository'),
    path('user/<str:username>/<str:repository>/remove', views.remove_repository, name='remove_repository'),
    path('user/<str:username>', views.user, name='user'),
    path('user/<str:username>/edit', views_logowanie.edit_profile, name='edit_profile'),
    path('user/<str:username>/<str:repository>', views.repository, name='repository'),
    path('user/<str:username>/<str:repository>/<str:parental_catalog>/add_catalog', views.add_catalog, name='add_catalog'),
    path('user/<str:username>/<str:repository>/<str:parental_catalog>', views.catalogs_and_files, name='catalogs_and_files'),
    path('user/<str:username>/<str:repository>/<str:parental_catalog>/<str:catalog>/delete_catalog', views.delete_catalog_and_files_within_it, name='delete_catalog')
]
