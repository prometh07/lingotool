#coding=utf-8
import json
import urllib
import urllib2

from django.http import HttpResponse

from .models import Word, WordSet

from conf import API_KEY


def generate_txt_file(word_sets):
    """
    Generate a .txt file from the list of WordSet pk's.
    """
    file_content = list()
    for word_set in word_sets:
        file_content.append(u'''Zestaw słówek - {}\n\n'''.format(word_set.title))
        for word in word_set.word_set.all().order_by('-difficulty'):
            file_content.append(u'''{} - {}\n'''.format(word.word, word.definition))
        file_content.append('\n')
    file_content = ''.join(file_content)
    return file_content


def get_dictionary_data(word):
    """Get a dictionary entry for given word.

    Args:
        word: the word to be searched.
    Returns:
        the dictionary entry in HTML format.

    """
    dict_code = 'british'
    headers = {
        'accessKey': API_KEY
    }
    params_dict = {
        'Accept': 'application/json',
        'format': 'html'
    }
    params = urllib.urlencode(params_dict)
    url = "".join(["https://dictionary.cambridge.org/api/v1/dictionaries/", dict_code, "/entries/", word.strip(), "/?", params])
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    data = response.read()
    data = json.loads(data)
    return data['entryContent']
