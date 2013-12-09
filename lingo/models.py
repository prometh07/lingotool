from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, DatabaseError


class Word(models.Model):
    """
    A word.
    """
    word = models.CharField(max_length=200)
    definition = models.CharField(max_length=500)
    difficulty = models.IntegerField()
    pos = models.CharField(max_length=64)
    word_set = models.ForeignKey('WordSet')

    def __unicode__(self):
        return unicode(self.word)


class WordSet(models.Model):
    """
    A set of words.
    """
    class Meta:
        ordering = ['-pub_date']

    title = models.CharField(max_length=500)
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
        Multiple definitions of the same words (i.e. having the same word and
        part of speech - pos - attributes) are merged.
        """
        for word_set in word_sets:
            for word in word_set.word_set.all():
                try:
                    similar_word = self.word_set.get(pos=word.pos, word=word.word)
                except ObjectDoesNotExist:
                    word.word_set = self
                    word.save()
                else:
                    try:
                        similar_word.definition += "; " + word.definition
                        similar_word.save()
                    except DatabaseError:
                        # definitions are too long to fit in one CharField;
                        # the word is deleted and definition lost (not probable)
                        pass
                    word.delete()
            word_set.delete()
        self.save()
