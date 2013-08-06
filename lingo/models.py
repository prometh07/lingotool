from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    word = models.CharField(max_length=128)
    definition = models.CharField(max_length=512)
    difficulty = models.IntegerField()
    word_set = models.ForeignKey('WordSet')

    def __unicode__(self):
        return unicode(self.word)


class WordSet(models.Model):
    title = models.CharField(max_length=1024)
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    words_number = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.title)
