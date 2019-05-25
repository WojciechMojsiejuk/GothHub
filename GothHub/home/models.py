from django.db import models
from logowanie.models import User


class Repository(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    class Meta():
        verbose_name_plural = "Repositories"

class Catalog(models.Model):
    name = models.CharField(max_length=128)
    repository_Id = models.ForeignKey(Repository, on_delete=models.CASCADE)
    parent_catalog = models.ForeignKey('Catalog', on_delete=models.CASCADE, null=True)

class File(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=128)
    extention = models.CharField(max_length=20)
    content = models.TextField()
    date_upload = models.DateField()
    repository_Id =  models.ForeignKey(Repository, on_delete=models.CASCADE)
    catalog_Id = models.ForeignKey(Catalog, on_delete=models.CASCADE)

class Version(models.Model):
    file_Id = models.ForeignKey(File, on_delete=models.CASCADE)
    version_nr = models.CharField(max_length=30)
    changes = models.TextField()
    date_modified: models.DateField()
