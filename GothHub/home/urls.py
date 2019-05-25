from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('user/<str:username>/add_repository', views.add_repository, name='add_repository'),
    path('user/<str:username>', views.user, name='user'),
    path('user/<str:username>/<str:repository>', views.repository, name='repository')
]
