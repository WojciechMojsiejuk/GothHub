from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.test import Client
from home.views import repository
from home.models import Repository as repo
from home.models import Catalog as catalog
from django.core.management import call_command

# Create your tests here.
class HomePageTest(TestCase):

    # creating instance of a client.
    def setUp(self):
        self.client = Client()
        call_command("loaddata", "' + 'programming_languages_definition.json' + '", verbosity=0)
    #HomePage should allow to create new repository
    def test_user_can_add_repository(self):
        repo.objects.create(name="MojeRepo",is_public=True)
        request=HttpRequest()
        response=repository(request)
        self.assertIn('MojeRepo',response.content.decode())

    #HomePage should allow to delete selected repository
    def test_user_can_delete_repository(self):
        repo.objects.create(name="MojeRepo",is_public=True)
        request=HttpRequest()
        response=repository(request)
        self.assertIn('MojeRepo',response.content.decode())
        #Checking if repository is still on site aftere deleting it
        repo.objects.all().delete()
        request=HttpRequest()
        response=repository(request)
        self.assertNotIn('MojeRepo',response.content.decode())


class HomePageCatalogTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.mojerepo=repo.objects.create(name="MojeRepo",is_public=True)

    #HomePage should allow to create new catalog
    def test_user_can_add_catalog_to_existing_repository(self):
        catalog.objects.create(name="Katalog1",repository_Id=self.mojerepo,parent_catalog=None)
