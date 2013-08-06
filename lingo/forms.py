#coding=utf-8
from django import forms
from lingo.models import WordSet, Word
from lingo.algorithms import naive, parse_text


class WordSetForm(forms.Form):
    title = forms.CharField(max_length=1024, required=False)
    file = forms.FileField(required=False)
    text = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        self.user = kwargs.pop('user', None)
        super(WordSetForm, self).__init__(*args, **kwargs)

    def clean(self):
        self.cleaned_data = super(WordSetForm, self).clean()
        if not self.cleaned_data.get('file') and not self.cleaned_data.get('text'):
            raise forms.ValidationError('Musisz wybrać plik albo wkleić tekst.')
        return self.cleaned_data

    def save(self):
        if not self.instance:
            self.instance = WordSet(
                title = self.cleaned_data.get('title'),
                user = self.user)
        file = self.cleaned_data.get('file')
        text = self.cleaned_data.get('text')
        data = file.read() if file else text
        data = parse_text(data)
        words = naive(data)
        self.instance.words_number += len(words)
        self.instance.save()
        for (word, word_val) in words:
            Word.objects.create(word=word, definition='', difficulty=word_val, word_set=self.instance)
