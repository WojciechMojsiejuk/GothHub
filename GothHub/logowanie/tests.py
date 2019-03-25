from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.test import Client

from logowanie.views import index

# Create your tests here.

class LoginPageTest(TestCase):
    
    # creating instance of a client.
    def setUp(self): 
        self.client = Client()
           
    def test_login_url_resolves_to_index_page_view(self):
        found = resolve('/login/')
        self.assertEqual(found.func, index)

    def test_login_page_returns_correct_html(self):
        response = self.client.post('/login/', {'username': 'john', 'password': 'smith'})
        
        #Login page should contain form where user can provide username and password
        self.assertIn(b'<form method="post">',response.content)
        self.assertIn(b'Username',response.content)
        self.assertIn(b'Password',response.content)
        self.assertIn(b'<button type="submit">Zaloguj</button>',response.content)
 
