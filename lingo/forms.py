#coding=utf-8
from django import forms

from .models import WordSet, Word
from .algorithms import naive, parse_text


class WordSetForm(forms.Form):
    """
    Form used to create a new WordSet or modify an exisiting one.
    """
    title = forms.CharField(max_length=1024, required=False)
    file = forms.FileField(required=False)
    text = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        self.user = kwargs.pop('user')
        super(WordSetForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(WordSetForm, self).clean()
        if not cleaned_data.get('file') and not cleaned_data.get('text'):
            raise forms.ValidationError('Musisz wybrać plik albo wkleić tekst.')
        if not self.instance and not cleaned_data.get('title'):
            raise forms.ValidationError('Musisz wpisać nazwę zestawu.')
        return cleaned_data

    def save(self):
        if not self.instance:
            self.instance = WordSet(title=self.cleaned_data.get('title'), user=self.user)
        file = self.cleaned_data.get('file')
        text = self.cleaned_data.get('text')
        data = file.read() if file else text
        words = parse_text(data)
        #words = naive(words)
        self.instance.save()
        word_difficulty = 0
        for (word, pos) in words:
            Word.objects.create(word=word, pos=pos, definition='',
                                difficulty=word_difficulty, word_set=self.instance)


class WordSetsListForm(forms.Form):
    """
    Form used to modify a list of WordSets.
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(WordSetsListForm, self).__init__(*args, **kwargs)
        self.fields['word_set'] = forms.ModelMultipleChoiceField(
            queryset=self.user.wordset_set.all(),
            widget=forms.widgets.CheckboxSelectMultiple)
        self.submit_action = self.data.get('submit_action', None)

    def save(self):
        word_sets = self.cleaned_data.get('word_set')
        if self.submit_action == 'delete':
            word_sets.delete()
        elif self.submit_action == 'merge':
            target = word_sets[0]
            target.merge(word_sets[1:])


class WordSetsDetailForm(forms.Form):
    """
    Form used to manage specific WordSet.
    """
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        self.user = kwargs.pop('user', None)
        super(WordSetsDetailForm, self).__init__(*args, **kwargs)
        self.fields['word'] = forms.ModelMultipleChoiceField(
            queryset=self.instance.word_set.all(),
            widget=forms.widgets.CheckboxSelectMultiple)
        self.submit_action = self.data.get('submit_action', None)

    def save(self):
        words = self.cleaned_data.get('word')
        if self.submit_action == 'delete':
            words.delete()
