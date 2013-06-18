from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    word = models.CharField(max_length=128)
    definition = models.CharField(max_length=512)
    word_set = models.ForeignKey('WordSet')

    def __unicode__(self):
        return unicode(self.word)


class WordSet(models.Model):
    title = models.CharField(max_length=1024)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return unicode(self.title)


