#!/usr/bin/env python
from lingo.frequency_list import freq_words

max_val = 10
easy_val = 2.0
medium_val = 6.0

def parse_text(text):
    words = [i.strip('()*&^%$#@!|\,.?/;:-_+=[]{}<>0123456789"\'') for i in text.split()]
    words = [i.lower() for i in words if len(i) > 2 and not i.isdigit()]
    words = list(set(words))
    words = [i for i in words if not '.' in i]
    return words

def naive(words):
    words = [[word, 0] for word in words]
    for word in words:
        if freq_words.get(word[0], max_val) <= easy_val:
            word[1] = 0 
        elif freq_words.get(word[0], max_val) <= medium_val:
            word[1] = 1
        else:
            word[1] = 2
    return words
