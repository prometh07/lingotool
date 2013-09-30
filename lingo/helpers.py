#coding=utf-8
from django.http import HttpResponse

from .models import Word, WordSet


def generate_txt_file(word_sets):
    response = HttpResponse(content_type='text/plain; charset=utf-8')
    for word_set in word_sets:
        response.write(u'''Zestaw słówek - {}\n\n'''.format(word_set.title))
        for word in word_set.word_set.all().order_by('-difficulty'):
            response.write(u'''{} - {}\n'''.format(word.word, word.definition))
        response.write('\n')
    response['Content-Disposition'] = 'attachment; filename="words.txt"'
    return response
