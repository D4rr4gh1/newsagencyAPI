from django.test import Client, TestCase
from .models import Author, Story
import requests

class LoginTestCase(TestCase):
    def test_login(self):
        r = requests.post('http://127.0.0.1:8000/login/', data = {'username':'darraghconnolly', 'password':'D@rtford1'})
        print(r.text)