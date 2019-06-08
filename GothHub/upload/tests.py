from django.test import TestCase
from django.test import Client
from home.models import File, Repository, Catalog, Version
from django.core.management import call_command

# Create your tests here.
class UploadPageTest(TestCase):

    def setUp(self):
        self.client = Client()
        repository = Repository.objects.create(name="Repozytorium", is_public=True)
        user = User.objects.create(username="User")
        catalog = Catalog.objects.create(name="Catalog", repository_Id=repository, parent_catalog=None)
        call_command("loaddata", "' + 'programming_languages_definition.json' + '", verbosity=0)
