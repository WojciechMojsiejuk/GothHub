from django.urls import path
from . import views

app_name = 'upload'
urlpatterns = [
    path('', views.upload, name = 'upload'),
    #path('download/', views.download, name='download')
]
