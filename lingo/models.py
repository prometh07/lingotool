from django.contrib.auth.models import User
from django.db import models


class Word(models.Model):
    """
    A word.
    """
    word = models.CharField(max_length=512)
    definition = models.CharField(max_length=512)
    difficulty = models.IntegerField()
    pos = models.CharField(max_length=64)
    word_set = models.ForeignKey('WordSet')

    def __unicode__(self):
        return unicode(self.word)


class WordSet(models.Model):
    """
    A set of words.
    """
    title = models.CharField(max_length=1024)
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.title)

    @property
    def words_number(self):
        """
        Return a number of words in the set of words.
        """
        return self.word_set.count()

    def merge(self, word_sets):
        """Merge other WordSets with self.

        Only one copy of the same words having identical definitions is saved.
        """
        for word_set in word_sets:
            for word in word_set.word_set.all():
                if not self.word_set.filter(word=word.word, definition=word.definition).exists():
                    word.word_set = self
                    word.save()
            word_set.delete()
        self.save()
