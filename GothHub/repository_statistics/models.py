from django.db import models


# Create your models here.
class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=128)
    # Language extensions should be separated with a comma
    extensions = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
