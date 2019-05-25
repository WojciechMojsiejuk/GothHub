from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('repository', views.repository, name='repository'),
    path('<str:username>', views.user, name='user'),
    path('<str:username>/<str:repository>', views.catalog, name='catalog')
]
