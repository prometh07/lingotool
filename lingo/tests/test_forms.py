import tempfile

from django.contrib.auth.models import User
from django.test import TestCase

from model_mommy import mommy

from ..models import Word, WordSet
from ..forms import WordSetsListForm, WordSetsDetailForm, WordSetForm


class WordSetFormTest(TestCase):
    def setUp(self):
        self.text = 'This is just a test sentence.'
        self.title = 'Test set'
        self.user = mommy.make(User)

    def test_valid_data_text(self):
        form = WordSetForm({'title': self.title, 'text': self.text}, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('title'), self.title)
        self.assertEqual(form.cleaned_data.get('text'), self.text)

        form.save()
        self.assertIsInstance(form.instance, WordSet)
        self.assertEqual(self.user.wordset_set.count(), 1)

#    def test_valid_data_file(self):
#        text = 'This is just a test sentence.'
#        filename = tempfile.mkstemp()[1]
#        f = open(filename, 'w')
#        f.write(text)
#        f.close()
#        f = open(filename, 'r')
#        title = 'Test set'
#        user = mommy.make(User)
#
#        form = WordSetForm({'title': title}, {'file': f}, user=user)
#        self.assertTrue(form.is_valid())
#        self.assertEqual(form.cleaned_data.get('title'), title)
#        self.assertEqual(form.cleaned_data.get('file'), text)
#
#        form.save()
#        self.assertIsInstance(form.instance, WordSet)
#        self.assertEqual(user.wordset_set.count(), 1)

    def test_invalid_data(self):
        # empty title
        form = WordSetForm({'title': '', 'text': self.text}, user=self.user)
        self.assertFalse(form.is_valid())
        # empty text
        form = WordSetForm({'title': self.title, 'text': ''}, user=self.user)
        self.assertFalse(form.is_valid())
        # empty title and text
        form = WordSetForm({'title': '', 'text': ''}, user=self.user)
        self.assertFalse(form.is_valid())


class WordSetsListFormTest(TestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.word_sets = mommy.make(WordSet, user=self.user, _quantity=3)
        for word_set in self.word_sets:
            mommy.make(Word, word_set=word_set, _quantity=3)

    def test_valid_data_delete(self):
        form = WordSetsListForm({'word_set': [self.word_sets[0].pk, self.word_sets[1].pk],
                                 'submit_action': 'delete'}, user=self.user)
        self.assertTrue(form.is_valid())
        #self.assertEqual(form.cleaned_data.get('word_set'), [self.word_sets[0], self.word_sets[1]])
        form.save()
        self.assertEqual(self.user.wordset_set.count(), 1) 

    def test_invalid_data_delete(self):
        another_user = mommy.make(User)
        another_word_set = mommy.make(WordSet, user=another_user)

        form = WordSetsListForm({'word_set': [another_word_set.pk],
                                 'submit_action': 'delete'}, user=self.user)
        self.assertFalse(form.is_valid())

    def test_valid_data_merge(self):
        form = WordSetsListForm({'word_set': [self.word_sets[0].pk, self.word_sets[1].pk],
                                 'submit_action': 'merge'}, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.user.wordset_set.count(), 2) 

    def test_invalid_data_merge(self):
        another_user = mommy.make(User)
        another_word_set = mommy.make(WordSet, user=another_user)

        form = WordSetsListForm({'word_set': [self.word_sets[0].pk, another_word_set.pk],
                                 'submit_action': 'merge'}, user=self.user)
        self.assertFalse(form.is_valid())


class WordSetsDetailFormTest(TestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.word_set = mommy.make(WordSet, user=self.user)
        self.words = mommy.make(Word, word_set=self.word_set, _quantity=10)

    def test_valid_data_delete(self):
        form = WordSetsDetailForm({'word': [self.words[0].pk, self.words[1].pk],
                                   'submit_action': 'delete'}, instance=self.word_set, 
                                   user=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.word_set.word_set.count(), 8) 

    def test_invalid_data_delete(self):
        another_user = mommy.make(User)
        another_word_set = mommy.make(WordSet, user=another_user)

        form = WordSetsDetailForm({'word': [self.words[0].pk, another_word_set.pk],
                                   'submit_action': 'delete'}, instance=self.word_set, 
                                   user=self.user)
        self.assertFalse(form.is_valid())
