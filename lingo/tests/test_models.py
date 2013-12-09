from django.test import TestCase

from model_mommy import mommy

from ..models import Word, WordSet


class WordTest(TestCase):
    def test_unicode(self):
        word = mommy.make(Word)
        self.assertEqual(word.__unicode__(), word.word)


class WordSetTest(TestCase):
    def setUp(self):
        self.word_set = mommy.make(WordSet)

    def test_unicode(self):
        self.assertEqual(self.word_set.__unicode__(), self.word_set.title)

    def test_words_number(self):
        words = mommy.make(Word, word_set=self.word_set, _quantity=50)
        self.assertEqual(self.word_set.words_number, 50)

    def test_merge(self):
        word_sets = mommy.make(WordSet, _quantity=10)
        for word_set in word_sets:
            mommy.make(Word, word_set=word_set, _quantity=10)

        # create another set containing duplicate words and append it to
        # word_sets
        duplicate_set = mommy.make(WordSet)
        for word in word_sets[0].word_set.all():
            mommy.make(Word, word=word.word, definition=word.definition,
                       difficulty=word.difficulty, pos=word.pos, word_set=duplicate_set)
        word_sets.append(duplicate_set)

        self.word_set.merge(word_sets)
        self.assertEqual(self.word_set.words_number, Word.objects.count())
        self.assertEqual(WordSet.objects.count(), 1)
