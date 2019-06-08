from django.http import HttpRequest, HttpResponseForbidden, Http404
from django.test import Client
from django.test import TestCase
from home.models import Repository, Catalog
from home.views import *
from home.forms import RepoCreationForm
from django.contrib.auth.models import User


# Create your tests here.
class HomePageTest(TestCase):

    # creating instance of a client.
    def setUp(self):
        self.client = Client()

    def test_template(self):
        self.response = self.client.get('')
        self.assertTemplateUsed(self.response, 'home.html')

    def test_home_page_returns_correct_response(self):
        self.response = self.client.get('')
        # Check that the response is 200 OK.
        self.assertEqual(self.response.status_code, 200)


class UsersProfilePageTest(TestCase):

    # creating instance of a client.
    def setUp(self):
        self.user = User.objects.create(username="JanKowalski")
        self.user.set_password('12345')
        self.user.save()
        self.client = Client()
        self.public_repository = Repository.objects.create(name="PubliczneRepozytoriumJanka", owner=self.user,
                                                           is_public=True)
        self.private_repository = Repository.objects.create(name="PrywatneRepozytoriumJanka", owner=self.user)

    def test_template(self):
        self.response = self.client.post('/user/' + str(self.user.username), {'username': self.user.username})
        self.assertTemplateUsed(self.response, 'users_profile.html')

    def test_users_profile_page_returns_correct_response(self):
        self.response = self.client.post('/user/' + str(self.user.username), {'username': self.user.username})
        self.assertEqual(self.response.status_code, 200)

    def test_users_profile_receive_non_existing_user(self):
        self.response = self.client.post('/user/' + str(self.user.username), {'username': "JanNowak"})
        self.assertRaises(Http404)

    def test_users_profile_everyone_can_see_only_users_public_repositories(self):
        self.response = self.client.post('/user/' + str(self.user.username), {'username': self.user.username})
        self.assertIn(b'PubliczneRepozytoriumJanka', self.response.content)
        self.assertNotIn(b'PrywatneRepozytoriumJanka', self.response.content)

    def test_users_profile_user_can_see_all_of_his_repositories(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.post('/user/' + str(self.user.username), {'username': self.user.username})
        self.assertIn(b'PubliczneRepozytoriumJanka', self.response.content)
        self.assertIn(b'PrywatneRepozytoriumJanka', self.response.content)


class AddRepositoryPage(TestCase):

    # creating instance of a client.
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
        self.private_repository = Repository.objects.create(name="PrywatneRepozytoriumJanka", owner=self.user)

    def test_template(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/add_repository')
        self.assertTemplateUsed(self.response, 'repository.html')

    def test_add_repository_page_returns_correct_response(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/add_repository')
        # Check that the response is 200 OK.
        self.assertEqual(self.response.status_code, 200)

    def test_view_doesnt_allow_to_add_repository_if_user_is_not_an_owner(self):
        self.client.login(username='JanNowak', password='54321')
        self.response = self.client.get('/user/' + str(self.user.username) + '/add_repository')
        self.assertEqual(self.response.status_code, 403)

    def test_add_repository_form_is_valid(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.post('/user/' + str(self.user.username + '/add_repository'),
                                         {'name': 'NowePubliczneRepozytorium', 'is_public': True})
        try:
            Repository.objects.filter(owner=self.user, name='NowePubliczneRepozytorium', is_public=True)
        except Repository.DoesNotExist:
            self.fail("Object was not created")

    def test_add_repository_form_is_not_valid(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.post('/user/' + str(self.user.username) + '/add_repository',
                                         {'name': 'NowePubliczneRepozytorium2', 'is_public': "NIE PRAWIDLOWE DANE"})

        self.assertEqual(Repository.objects.filter(owner=self.user, name='NowePubliczneRepozytorium2').count(), 0)

    def test_add_repository_shouldnt_allow_to_add_repository_with_already_existing_name(self):
        Repository.objects.create(owner=self.user, name="ToSamoRepozytorium", is_public=True)
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.post('/user/' + str(self.user.username + '/add_repository'),
                                         {'name': 'ToSamoRepozytorium', 'is_public': True})
        # form should not create another Repository objects
        self.assertEqual(
            Repository.objects.filter(owner=self.user, name="ToSamoRepozytorium", is_public=True).count(),
            1)


class RepositoryPage(TestCase):

    # creating instance of a client.
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
        self.private_repository = Repository.objects.create(name="PrywatneRepozytoriumJanka", owner=self.user)

    def test_template(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.public_repository.name))
        self.assertTemplateUsed(self.response, 'repository_catalogs_and_files.html')

    def test_repository_page_returns_correct_response(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.public_repository.name))
        # Check that the response is 200 OK.
        self.assertEqual(self.response.status_code, 200)

    def test_incorrect_user(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/jankowalski/' + str(self.public_repository.name))
        self.assertRaises(Http404)

    def test_other_user_tries_to_see_private_repository(self):
        self.client.login(username='JanNowak', password='54321')
        self.response = self.client.get('/user/+ str(self.user.username)' + '/' + str(self.private_repository.name))
        self.assertRaises(Http404)

    def test_user_tries_to_see_not_existing_repository(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/+ str(self.user.username)' + '/NieIstniejaceRepozytorium')
        self.assertRaises(Http404)

    def test_user_receives_correct_repository(self):
        self.client.login(username='JanKowalski', password='12345')
        self.catalog = Catalog.objects.create(name='KatalogJanka', repository_Id=self.public_repository, parent_catalog=None)
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.public_repository.name))
        self.assertEqual(self.response.context['repository'], self.public_repository)
        self.assertEqual(self.response.context['catalogs'][0], self.catalog)


class DeleteRepositoryPage(TestCase):

    # creating instance of a client.
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

    def test_delete_repository_page_returns_correct_response(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.public_repository.name) +'/delete_repository')
        # Check that the response is 302 = redirect.
        self.assertEqual(self.response.status_code, 302)

    def test_delete_repository_shouldnt_allow_to_delete_repository_if_user_is_not_an_owner(self):
        self.client.login(username='JanNowak', password='54321')
        self.response = self.client.get(
            '/user/' + str(self.user.username) + '/' + str(self.public_repository.name) + '/delete_repository')
        # Check that the response is 403 = forbidden.
        self.assertEqual(self.response.status_code, 403)

    def test_incorrect_user(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get(
            '/user/jankowalski/' + str(self.public_repository.name) + '/delete_repository')
        self.assertRaises(Http404)

    def test_user_deletes_repository(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get(
            '/user/' + str(self.user.username) + '/' + str(self.public_repository.name) + '/delete_repository')
        self.assertEqual(
            Repository.objects.filter(name="PubliczneRepozytoriumJanka", owner=self.user, is_public=True).count(),
            0)

    def test_trying_to_delete_not_existing_repository(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get(
            '/user/' + str(self.user.username) + '/PrywatneRezpozytoriumJanka' + '/delete_repository')
        self.assertRaises(Http404)


class AddCatalogPage(TestCase):

    # creating instance of a client.
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

    def test_template(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.public_repository.name)+'/add_catalog')
        self.assertTemplateUsed(self.response, 'catalog.html')

    def test_add_catalog_page_returns_correct_response(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.public_repository.name)+'/add_catalog')
        # Check that the response is 200 OK.
        self.assertEqual(self.response.status_code, 200)

    def test_incorrect_user(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.public_repository.name)+'/add_catalog')
        self.assertRaises(Http404)

    def test_add_catalog_shouldnt_allow_to_add_catalog_if_user_is_not_an_owner(self):
        self.client.login(username='JanNowak', password='54321')
        self.response = self.client.get(
            '/user/' + str(self.user.username) + '/' + str(self.public_repository.name) + '/add_catalog')
        # Check that the response is 403 = forbidden.
        self.assertEqual(self.response.status_code, 403)

    def test_user_adds_catalog(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.post(
            '/user/' + str(self.user.username) + '/' + str(self.public_repository.name) + '/add_catalog',
            {'name': 'KatalogJanka'})
        self.assertEqual(Catalog.objects.filter(name="KatalogJanka", repository_Id=self.public_repository).count(), 1)

    def test_trying_to_add_already_existing_catalog(self):
        self.client.login(username='JanKowalski', password='12345')
        Catalog.objects.create(name="KatalogJanka", repository_Id=self.public_repository, parent_catalog=None)
        self.response = self.client.post(
            '/user/' + str(self.user.username) + '/' + str(self.public_repository.name) + '/add_catalog',
            {'name': 'KatalogJanka'})
        self.assertNotEqual(Catalog.objects.filter(name="KatalogJanka", repository_Id=self.public_repository).count(), 2)

'''        
class HomePageCatalogTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.mojerepo=repo.objects.create(name="MojeRepo",is_public=True)

    #HomePage should allow to create new catalog
    def test_user_can_add_catalog_to_existing_repository(self):
        catalog.objects.create(name="Katalog1",repository_Id=self.mojerepo,parent_catalog=None)


    # HomePage should allow to create new repository
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
        self.assertNotIn('MojeRepo',response.content.decode())'''
