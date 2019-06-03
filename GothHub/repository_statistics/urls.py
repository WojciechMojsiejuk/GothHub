from django.urls import path
from . import views

app_name = 'repository_statistics'
urlpatterns = [
    path('', views.show_statistics, name='show_statistics')
]
