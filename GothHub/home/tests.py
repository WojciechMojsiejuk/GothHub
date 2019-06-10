from django.http import HttpRequest, HttpResponseForbidden, Http404
from django.test import Client
from django.test import TestCase
from home.models import Repository, Catalog, File, Version
from home.views import *
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

    # def test_add_repository_form_is_not_valid(self):
    #     self.client.login(username='JanKowalski', password='12345')
    #     self.response = self.client.post('/user/' + str(self.user.username) + '/add_repository',
    #                                      {'name': 'NowePubliczneRepozytorium2', 'is_public': 123})
    #
    #     self.assertEqual(Repository.objects.filter(owner=self.user, name='NowePubliczneRepozytorium2').count(), 0)

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
        self.catalog = Catalog.objects.create(name='KatalogJanka', repository_Id=self.public_repository,
                                              parent_catalog=None)
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
        self.response = self.client.get(
            '/user/' + str(self.user.username) + '/' + str(self.public_repository.name) + '/delete_repository')
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
        self.response = self.client.get(
            '/user/' + str(self.user.username) + '/' + str(self.public_repository.name) + '/add_catalog')
        self.assertTemplateUsed(self.response, 'catalog.html')

    def test_add_catalog_page_returns_correct_response(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get(
            '/user/' + str(self.user.username) + '/' + str(self.public_repository.name) + '/add_catalog')
        # Check that the response is 200 OK.
        self.assertEqual(self.response.status_code, 200)

    def test_incorrect_user(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get(
            '/user/' + str(self.user.username) + '/' + str(self.public_repository.name) + '/add_catalog')
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
        self.assertNotEqual(Catalog.objects.filter(name="KatalogJanka", repository_Id=self.public_repository).count(),
                            2)


class CatalogsAndFilesPage(TestCase):

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
        self.users_parental_catalog = Catalog.objects.create(
            name="KatalogJanka1",
            repository_Id=self.public_repository,
            parent_catalog=None)
        self.users_catalog = Catalog.objects.create(
            name="KatalogJanka2",
            repository_Id=self.public_repository,
            parent_catalog=self.users_parental_catalog)
        self.users_file = File.objects.create(
            author=self.user,
            file_name="PlikJanka",
            repository_Id=self.public_repository,
            catalog_Id=self.users_parental_catalog
        )

    def test_template(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' +
                                        str(self.public_repository.name) + '/' + str(self.users_parental_catalog))
        self.assertTemplateUsed(self.response, 'repository_catalogs_and_files.html')

    def test_add_catalog_page_returns_correct_response(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' +
                                        str(self.public_repository.name) + '/' + str(self.users_parental_catalog))
        # Check that the response is 200 OK.
        self.assertEqual(self.response.status_code, 200)

    def test_incorrect_user(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/jankowalski/' +
                                        str(self.public_repository.name) + '/' + str(self.users_parental_catalog))
        self.assertRaises(Http404)

    def test_invalid_repository_owner(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/ZlaNazwa/' +
                                        str(self.users_parental_catalog))
        self.assertRaises(Http404)

    def test_invalid_repository_others(self):
        self.client.login(username='JanNowak', password='54321')
        self.response = self.client.get('/user/' + str(self.user.username) + '/ZlaNazwa/' +
                                        str(self.users_parental_catalog))
        self.assertRaises(Http404)

    def test_invalid_catalog(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' +
                                        str(self.public_repository.name) + '/ZlaNazwa')
        self.assertRaises(Http404)

    def test_users_gets_catalogs_and_files(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' +
                                        str(self.public_repository.name) + '/' + str(self.users_parental_catalog))
        self.assertTemplateUsed(self.response, 'repository_catalogs_and_files.html')
        self.assertEqual(self.response.context['files'][0]['file_name'], self.users_file.file_name)
        self.assertEqual(self.response.context['catalogs'][0], self.users_catalog)


class DeleteCatalogPage(TestCase):

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
        self.users_parental_catalog = Catalog.objects.create(
            name="KatalogJanka1",
            repository_Id=self.public_repository,
            parent_catalog=None)
        self.users_catalog = Catalog.objects.create(
            name="KatalogJanka2",
            repository_Id=self.public_repository,
            parent_catalog=self.users_parental_catalog)
        self.users_file = File.objects.create(
            author=self.user,
            file_name="PlikJanka",
            repository_Id=self.public_repository,
            catalog_Id=self.users_parental_catalog
        )

    def test_delete_catalog_page_returns_correct_response(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' +
                                        str(self.public_repository.name) + '/' +
                                        str(self.users_parental_catalog) + '/' +
                                        str(self.users_catalog)+'/delete_catalog')

        # Check that the response is 302 = Redirect.
        self.assertEqual(self.response.status_code, 302)

    def test_incorrect_user(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' +
                                        str(self.public_repository.name) + '/' +
                                        str(self.users_parental_catalog) + '/' +
                                        str(self.users_catalog) + '/delete_catalog')
        self.assertRaises(Http404)

    def test_delete_catalog_shouldnt_allow_to_delete_catalog_if_user_is_not_an_owner(self):
        self.client.login(username='JanNowak', password='54321')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' +
                                        str(self.public_repository.name) + '/' +
                                        str(self.users_parental_catalog) + '/' +
                                        str(self.users_catalog) + '/delete_catalog')
        # Check that the response is 401 = unauthorized.
        self.assertEqual(self.response.status_code, 401)

    def test_user_delete_catalog(self):
        self.client.login(username='JanNowak', password='54321')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' +
                                        str(self.public_repository.name) + '/' +
                                        str(self.users_parental_catalog) + '/' +
                                        str(self.users_catalog) + '/delete_catalog')
        self.assertEqual(Catalog.objects.filter(repository_Id=self.public_repository).count(), 1)
        self.assertEqual(Catalog.objects.filter(repository_Id=self.public_repository, name=self.users_catalog).count(), 0)
        self.assertEqual(Catalog.objects.filter(repository_Id=self.public_repository, name=self.users_parental_catalog).count(), 1)

class ShowFilePage(TestCase):

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

        self.users_parental_catalog = Catalog.objects.create(
            name="KatalogJanka1",
            repository_Id=self.public_repository,
            parent_catalog=None
        )
        self.users_catalog = Catalog.objects.create(
            name="KatalogJanka2",
            repository_Id=self.public_repository,
            parent_catalog=self.users_parental_catalog
        )
        self.users_priv_catalog = Catalog.objects.create(
            name="KatalogJanka3",
            repository_Id=self.private_repository,
            parent_catalog=None
        )
        self.users_file_1 = File.objects.create(
            author=self.user,
            file_name="PlikJanka",
            repository_Id=self.public_repository,
            catalog_Id=self.users_catalog
        )
        self.users_file_1_version = Version.objects.create(
            file_Id=self.users_file_1,
            version_nr=1
        )
        self.users_file_2 = File.objects.create(
            author=self.user,
            file_name="PlikJanka",
            repository_Id=self.public_repository,
            catalog_Id=self.users_catalog
        )
        self.users_file_2_version = Version.objects.create(
            file_Id=self.users_file_2,
            version_nr=2
        )
        self.users_file_3 = File.objects.create(
            author=self.user,
            file_name="PlikJanka",
            repository_Id=self.private_repository,
            catalog_Id=self.users_priv_catalog
        )
        self.users_file_3_version = Version.objects.create(
            file_Id=self.users_file_3,
            version_nr=1
        )
        f = open('media/files/' + str(self.users_file_1.file_name), 'w')
        f.write('Plik 1')
        f.close()
        f2 = open('media/files/' + str(self.users_file_2.file_name), 'w')
        f2.write('Plik 2')
        f2.close()
        f3 = open('media/files/' + str(self.users_file_3.file_name), 'w')
        f3.write('Plik 3')
        f3.close()

    def test_template(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.public_repository.name) +
                                        '/' + str(self.users_parental_catalog) + '/' + str(self.users_catalog) +
                                        '/files/' + str(self.users_file_1.file_name) + '/' +
                                        str(self.users_file_1_version.version_nr))
        self.assertTemplateUsed(self.response, 'file.html')

    def test_show_file_page_returns_correct_response(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.public_repository.name) +
                                        '/' + str(self.users_parental_catalog) + '/' + str(self.users_catalog) +
                                        '/files/' + str(self.users_file_1.file_name) + '/' +
                                        str(self.users_file_1_version.version_nr))
        # Check that the response is 200 OK.
        self.assertEqual(self.response.status_code, 200)

    def test_incorrect_user(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/jankowalski/' + str(self.public_repository.name) +
                                        '/' + str(self.users_parental_catalog) + '/' + str(self.users_catalog) +
                                        '/files/' + str(self.users_file_1.file_name) + '/' +
                                        str(self.users_file_1_version.version_nr))
        self.assertRaises(Http404)

    def test_invalid_repository(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/ZlaNazwa/' +
                                        str(self.users_parental_catalog) + '/' + str(self.users_catalog) +
                                        '/files/' + str(self.users_file_1.file_name) + '/' +
                                        str(self.users_file_1_version.version_nr))
        self.assertRaises(Http404)

    def test_invalid_catalog(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.public_repository.name) +
                                        '/ZlaNazwa/' + str(self.users_catalog) +
                                        '/files/' + str(self.users_file_1.file_name) + '/' +
                                        str(self.users_file_1_version.version_nr))
        self.assertRaises(Http404)
    def test_other_user_can_see_file_if_repository_is_public(self):
        self.client.login(username='JanNowak', password='54321')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.public_repository.name) +
                                        '/' + str(self.users_parental_catalog) + '/' + str(self.users_catalog) +
                                        '/files/' + str(self.users_file_1.file_name) + '/' +
                                        str(self.users_file_1_version.version_nr))
        self.assertEqual(self.response.status_code, 200)

    def test_other_user_cant_see_file_if_repository_is_private(self):
        self.client.login(username='JanNowak', password='54321')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.private_repository.name) +
                                        '/' + str(self.users_priv_catalog) +
                                        '/files/' + str(self.users_file_3.file_name) + '/' +
                                        str(self.users_file_3_version.version_nr))
        self.assertEqual(self.response.status_code, 401)

    def test_latest_version_files_1_and_2(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.public_repository.name) +
                                        '/' + str(self.users_parental_catalog) + '/' + str(self.users_catalog) +
                                        '/files/' + str(self.users_file_1.file_name) + '/latest')
        self.assertEqual(self.response.context['versions'].latest('version_nr').version_nr, self.users_file_2_version.version_nr)

    def test_latest_version_file_3(self):
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.private_repository.name) +
                                        '/' + str(self.users_priv_catalog) +
                                        '/files/' + str(self.users_file_3.file_name) + '/latest')
        self.assertEqual(self.response.context['versions'].latest('version_nr').version_nr, 1)

    def test_correct_version_file_1(self):
        f = open('media/files/' + str(self.users_file_1.file_name), 'w')
        f.write('Plik 1')
        f.close()
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.public_repository.name) +
                                        '/' + str(self.users_parental_catalog) + '/' + str(self.users_catalog) +
                                        '/files/' + str(self.users_file_1.file_name) + '/' +
                                        str(self.users_file_1_version.version_nr))
        self.assertEqual(self.response.context['file_content'], "Plik 1")

    def test_correct_version_file_2(self):
        f2 = open('media/files/' + str(self.users_file_2.file_name), 'w')
        f2.write('Plik 2')
        f2.close()
        self.client.login(username='JanKowalski', password='12345')
        self.response = self.client.get('/user/' + str(self.user.username) + '/' + str(self.public_repository.name) +
                                        '/' + str(self.users_parental_catalog) + '/' + str(self.users_catalog) +
                                        '/files/' + str(self.users_file_2.file_name) + '/' +
                                        str(self.users_file_2_version.version_nr))
        self.assertEqual(self.response.context['file_content'], "Plik 2")