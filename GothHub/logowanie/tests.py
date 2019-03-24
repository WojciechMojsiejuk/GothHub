from django.test import TestCase
from django.urls import resolve
from logowanie.views import index
# Create your tests here.

class LoginPageTest(TestCase):
    def test_login_url_resolves_to_index_page_view(self):
        found = resolve('/login/')
        self.assertEqual(found.func, index)
