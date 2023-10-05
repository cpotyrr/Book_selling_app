import json
import unittest

from django.contrib.auth.models import User

# Create your tests here.
from rest_framework.test import force_authenticate, APIClient

from book_selling.models import Book, Author


class TestBookSelling(unittest.TestCase):
    def setUp(self):
        self.test_client = APIClient()
        self.username = 'test_user'
        self.password = 'very_hard_password'
        self.test_client.post('/auth/users/', data={'username': self.username, 'password': self.password})
        self.access_token = json.loads(self.test_client.post('/auth/jwt/create/', data={'username': self.username,
                                                                                        'password': self.password}).content.decode(
            'utf-8'))['access']
        self.test_client.force_authenticate(user=User.objects.get(is_superuser=True), token=self.access_token)

    def test_succesfully_auth(self):
        response = self.test_client.get('/auth/users/me/')
        self.assertEqual(response.status_code, 200)

    def test_get_book(self):
        response = self.test_client.get('/books/', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_authors(self):
        response = self.test_client.get('/authors/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
