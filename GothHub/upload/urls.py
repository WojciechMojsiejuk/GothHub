from django.urls import path
from . import views

app_name = 'upload'
urlpatterns = [
    path('user/<str:username>/<str:repository>/<str:parental_catalog>/<str:catalog>/upload', views.upload_file, name='upload'),
]
