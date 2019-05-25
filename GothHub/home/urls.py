from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('repository', views.repository, name='repository'),
    path('user/<str:username>/<str:repository>/addcatalog', views.newcatalog, name='catalog'),
    path('user/<str:username>', views.user, name='user')
]
