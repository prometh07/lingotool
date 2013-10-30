from django.contrib.auth.models import User
from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=512)
    definition = models.CharField(max_length=512)
    difficulty = models.IntegerField()
    word_set = models.ForeignKey('WordSet')

    def __unicode__(self):
        return unicode(self.word)


class WordSet(models.Model):
    title = models.CharField(max_length=1024)
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.title)

    @property
    def words_number(self):
        return self.word_set.count()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    class Meta:
        permissions = (
            ('is_tester', 'true'),
        )
