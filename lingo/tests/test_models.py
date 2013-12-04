from django.test import TestCase
from lingo.models import Word, WordSet

from model_mommy import mommy


class WordTest(TestCase):
    def test_word(self):
        word = mommy.make(Word)
        self.assertEqual(word.__unicode__(), word.word)


class WordSetTest(TestCase):
    def test_word_set(self):
        word_set = mommy.make(WordSet)
        self.assertEqual(word_set.__unicode__(), word_set.title)

