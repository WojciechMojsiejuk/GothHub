from django.test import TestCase
from django.urls import resolve, reverse
from django.http import HttpRequest
from django.test import Client

from logowanie.views import index
from logowanie.views import signup
from .forms import *
from django.core.management import call_command

# Create your tests here.


class LoginPageTest(TestCase):

    # creating instance of a client.
    def setUp(self):
        self.client = Client()
        call_command("loaddata", "' + 'programming_languages_definition.json' + '", verbosity=0)

    def test_login_url_resolves_to_index_page_view(self):
        found = resolve('/login/')
        self.assertEqual(found.func, index)

    def test_login_page_returns_correct_html(self):
        response = self.client.post('/login/', {'username': 'john', 'password': 'smith'})

        # Login page should contain form where user can provide username and password
        self.assertIn(b'<form method="post">',response.content)
        self.assertIn(b'Username',response.content)
        self.assertIn(b'Password',response.content)
        self.assertIn(b'<button type="submit">Zaloguj</button>',response.content)

    def test_user_can_login_to_his_home_page_by_valid_form(self):
        self.user = User.objects.create(username="JanKowalski", email="jankowalski@gmail.com", password="Haslo_to_okon")
        form = LoginForm(data={'username': 'JanKowalski', 'password': 'Haslo_to_okon'})
        self.assertTrue(form.is_valid())
        response = self.client.get(reverse('logowanie:home'))
        self.assertEqual(response.status_code, 200)


class RegistrationPageTest(TestCase):

    # creating instance of a client.
    def setUp(self):
        self.client = Client()

    def test_join_url_resolves_to_signup_page_view(self):
        found = resolve('/join/')
        self.assertEqual(found.func, signup)

    def test_signup_page_returns_correct_html(self):
        # SignUp page should contain form where user can provide username, email and password
        response = self.client.get('/join/')
        self.assertIn(b'<form method="post">', response.content)
        self.assertIn(b'Username', response.content)
        self.assertIn(b'Email', response.content)
        self.assertIn(b'Password', response.content)
        self.assertIn(b'<button type="submit">Zaloguj</button>', response.content)

    def test_signup_page_generates_token(self):
        pass
        #response = self.client.post('/join/', {'username':'jan', 'email':'jankowalski@gmail.com', 'password1':'Haslo_to_okon', 'password2':'Haslo_to_okon'})

    def test_signup_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        response = signup(request)
        pass
