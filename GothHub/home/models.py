from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from logowanie.models import User


class Repository(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Repositories"


class Catalog(models.Model):
    name = models.CharField(max_length=128)
    repository_Id = models.ForeignKey(Repository, on_delete=models.CASCADE)
    parent_catalog = models.ForeignKey('Catalog', on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.name


class File(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=128)
    extension = models.CharField(max_length=20)
    date_upload = models.DateTimeField(auto_now_add=True, blank=True)
    repository_Id = models.ForeignKey(Repository, on_delete=models.CASCADE)
    catalog_Id = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    dir = models.FileField(upload_to='files/')

    def __str__(self):
        return self.file_name


@receiver(post_delete, sender=File)
def file_delete(sender, instance, **kwargs):
    instance.dir.delete(False)


class Version(models.Model):
    file_Id = models.ForeignKey(File, on_delete=models.CASCADE)
    version_nr = models.IntegerField()
    date_modified: models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.file_Id.file_name) + " Version: " + str(self.version_nr)