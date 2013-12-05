from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from model_mommy import mommy

from ..models import Word, WordSet


class WordSetsListTest(TestCase):
    def setUp(self):
        self.url = reverse('word_sets_list')
        self.user = mommy.make(User, password=make_password('test'))

    def test_anonymous(self):
        response = self.client.get(self.url)
        expected_url = '/accounts/login/?next=/word_sets/'
        self.assertRedirects(response, expected_url) 
        
        response = self.client.post(self.url)
        self.assertRedirects(response, expected_url) 

    def test_user(self):
        login = self.client.login(username=self.user.username, password='test')
        self.assertEqual(login, True)
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_delete(self):
        login = self.client.login(username=self.user.username, password='test')
        self.assertEqual(login, True)

        word_sets = mommy.make(WordSet, user=self.user, _quantity=3) 
        #response = self.client.post(self.url, data={ })
