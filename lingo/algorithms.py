from collections import defaultdict

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize

from .frequency_list import freq_words


wordnet_pos_tags = defaultdict(str, J='a', V='v', N='n', R='r')

max_val = 10
easy_val = 2.0
medium_val = 6.0


def parse_text(text):
    """
    Parse the given text using nltk library.

    Args:
        text: the text to be parsed.
    Returns:
        the list of tuples (word, part_of_speech)
    """
    sentences = sent_tokenize(text)
    sentences = [word_tokenize(sent) for sent in sentences]
    words = [word.strip() for sent in sentences for word in sent]
    words = [word for word in words if len(word) > 2 and not word.isdigit()]
    words = pos_tag(words)
    lemmatizer = WordNetLemmatizer()
    for i, (word, pos) in enumerate(words):
        wordnet_pos = wordnet_pos_tags[pos[0]]
        if wordnet_pos:
            words[i] = (lemmatizer.lemmatize(word, pos=wordnet_pos), wordnet_pos)
    words = [(word, pos) for word, pos in words if len(word) > 2]
    words = list(set(words))
    return words


def naive(words):
    words = [[word, pos, 0] for word, pos in words]
    for word in words:
        if freq_words.get(word[0], max_val) <= easy_val:
            word[2] = 0
        elif freq_words.get(word[0], max_val) <= medium_val:
            word[2] = 1
        else:
            word[2] = 2
    return words
