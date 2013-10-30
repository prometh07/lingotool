#coding=utf-8
import json
import urllib
import urllib2

from django.http import HttpResponse

from .models import Word, WordSet

from conf import API_KEY


def generate_txt_file(word_sets):
    file_content = list()
    for word_set in word_sets:
        file_content.append(u'''Zestaw słówek - {}\n\n'''.format(word_set.title))
        for word in word_set.word_set.all().order_by('-difficulty'):
            file_content.append(u'''{} - {}\n'''.format(word.word, word.definition))
        file_content.append('\n')
    file_content = ''.join(file_content)
    return file_content


def get_dictionary_data(word):
    dict_code = 'british'
    url = "".join(["https://dictionary.cambridge.org/api/v1/dictionaries/", dict_code, "/search"])
    headers = {
        'Accept': 'application/json'
    }
    params_dict = {
        'accessKey': API_KEY,
        'pageindex': '1',
        'pagesize': '10',
        'q': word
    }
    params = urllib.urlencode(params_dict)
    request = urllib2.Request(url, params, headers=headers)
    response = urllib2.urlopen(request)
    data = response.read()
    return data
