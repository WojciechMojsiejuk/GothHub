from django.test import TestCase
from django.test import Client
from home.models import File, Repository, Catalog, Version
from django.core.management import call_command

# Create your tests here.
class UploadPageTest(TestCase):

    def setUp(self):
        # user which repositories are tested
        self.user = User.objects.create(username="JanKowalski")
        self.user.set_password('12345')
        self.user.save()
        # other user
        self.user2 = User.objects.create(username="JanNowak")
        self.user2.set_password('54321')
        self.user2.save()

        self.client = Client()
        self.public_repository = Repository.objects.create(name="PubliczneRepozytoriumJanka", owner=self.user,
                                                           is_public=True)
