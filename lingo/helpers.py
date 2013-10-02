#coding=utf-8
from django.http import HttpResponse

from .models import Word, WordSet


def generate_txt_file(word_sets):
    file_content = list()
    for word_set in word_sets:
        file_content.append(u'''Zestaw słówek - {}\n\n'''.format(word_set.title))
        for word in word_set.word_set.all().order_by('-difficulty'):
            file_content.append(u'''{} - {}\n'''.format(word.word, word.definition))
        file_content.append('\n')
    file_content = ''.join(file_content)
    return file_content
