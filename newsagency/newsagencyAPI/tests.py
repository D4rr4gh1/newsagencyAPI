from django.test import Client, TestCase
from .models import Author, Story
import requests

class LoginTestCase(TestCase):
    def test_login(self):
        r = requests.post('http://127.0.0.1:8000/api/login', data = {'username':'darraghconnolly', 'password':'D@rtford1'})
        print(r.text)

class StoriesTestCase(TestCase):
    session = requests.Session()
    # def setUp(self):
    #     response = self.session.post('http://127.0.0.1:8000/api/login', data = {'username':'darraghconnolly', 'password':'D@rtford1'})
    #     self.assertEqual(response.status_code, 200)

    # def test_post_stories(self):
    #     response = self.session.post('http://127.0.0.1:8000/api/stories',json={"headline": "Shit happened", "category": "pol", "region": "uk", "details": "I did some work for once"})
    #     print(response.text)
    #     self.assertEqual(response.status_code, 201)

    # def test_logout(self):
    #     response = self.session.post('http://127.0.0.1:8000/api/logout')
    #     self.assertEqual(response.status_code, 200)

    # def test_get(self):
    #     response = self.session.get('http://127.0.0.1:8000/api/stories', data={'story_cat' : 'pol', 'story_region' : '*', 'story_date' : '*'})
    #     print(response.text)

    def test_acc2_login(self):
        response = self.session.post('http://127.0.0.1:8000/api/login', data = {'username':'ammar', 'password':'webServices123'})
        self.assertEqual(response.status_code, 200)
    
    def test_acc2_delete_from_acc1(self):
        response = self.session.delete('http://127.0.0.1:8000/api/stories/1')
        print(response.text)

