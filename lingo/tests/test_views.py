#encoding=utf-8
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core import mail
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
        another_user = mommy.make(User)
        another_word_set = mommy.make(WordSet, user=another_user)
        # valid POST data
        response = self.client.post(self.url, {
            'word_set': word_sets[-1].pk,
            'submit_action': 'delete',
        })
        self.assertEqual(response.status_code, 302)
        # invalid POST data
        response = self.client.post(self.url, {
            'word_set': another_word_set.pk,
            'submit_action': 'delete',
        })
        self.assertEqual(response.status_code, 302)

    def test_merge(self):
        login = self.client.login(username=self.user.username, password='test')
        self.assertEqual(login, True)

        word_sets = mommy.make(WordSet, user=self.user, _quantity=3) 
        another_user = mommy.make(User)
        another_word_set = mommy.make(WordSet, user=another_user)
        # valid POST data
        response = self.client.post(self.url, {
            'word_set': word_sets[-1].pk,
            'word_set': word_sets[-2].pk,
            'submit_action': 'merge',
        })
        self.assertEqual(response.status_code, 302)
        # invalid POST data
        response = self.client.post(self.url, {
            'word_set': another_word_set.pk,
            'word_set': word_sets[-1].pk,
            'submit_action': 'merge',
        })
        self.assertEqual(response.status_code, 302)

    def test_download_txt(self):
        login = self.client.login(username=self.user.username, password='test')
        self.assertEqual(login, True)

        word_sets = mommy.make(WordSet, user=self.user, _quantity=3) 
        another_user = mommy.make(User)
        another_word_set = mommy.make(WordSet, user=another_user)
        # valid POST data
        response = self.client.post(self.url, {
            'word_set': word_sets[-1].pk,
            'submit_action': 'download_txt',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'text/plain; charset=utf-8')
        # invalid POST data
        response = self.client.post(self.url, {
            'word_set': another_word_set.pk,
            'submit_action': 'download_txt',
        })
        self.assertEqual(response.status_code, 302)

    def test_download_email(self):
        login = self.client.login(username=self.user.username, password='test')
        self.assertEqual(login, True)

        word_sets = mommy.make(WordSet, user=self.user, _quantity=3) 
        another_user = mommy.make(User)
        another_word_set = mommy.make(WordSet, user=another_user)
        # valid POST data
        response = self.client.post(self.url, {
            'word_set': word_sets[-1].pk,
            'submit_action': 'download_email',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Zestawy słówek')
        # invalid POST data
        response = self.client.post(self.url, {
            'word_set': another_word_set.pk,
            'submit_action': 'download_email',
        })
        self.assertEqual(response.status_code, 302)


class WordSetsDetailTest(TestCase):
    def setUp(self):
        self.user = mommy.make(User, password=make_password('test'))
        self.word_set = mommy.make(WordSet, user=self.user)
        self.words = mommy.make(Word, word_set=self.word_set, _quantity=10)
        self.url = reverse('word_sets_detail', args=(self.word_set.pk,))

    def test_anonymous(self):
        response = self.client.get(self.url)
        expected_url = '/accounts/login/?next=/word_sets/{}/'.format(self.word_set.pk)
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

    def test_download_txt(self):
        login = self.client.login(username=self.user.username, password='test')
        self.assertEqual(login, True)

        another_user = mommy.make(User)
        another_word_set = mommy.make(WordSet, user=another_user)
        # always valid - file contains WordSet requested in url
        response = self.client.post(self.url, {
            'submit_action': 'download_txt',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'text/plain; charset=utf-8')

    def test_download_email(self):
        login = self.client.login(username=self.user.username, password='test')
        self.assertEqual(login, True)

        another_user = mommy.make(User)
        another_word_set = mommy.make(WordSet, user=another_user)
        response = self.client.post(self.url, {
            'submit_action': 'download_email',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Zestawy słówek')
