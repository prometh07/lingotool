#coding=utf-8
import time

from django.core.mail import EmailMessage
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from google.appengine.ext import db

from conf import EMAIL_HOST_USER
from .forms import WordSetForm
from .models import Word, WordSet


def login_user(request, *args, **kwargs):
    if request.POST.get('remember_me'):
        request.session.set_expiry(604800)
    return auth_views.login(request, *args, **kwargs)


@login_required
def word_sets_list(request):
    if request.method == 'POST':
        word_sets = request.user.wordset_set.filter(pk__in=request.POST.getlist('word_set'))
        if request.POST.get('submit_action') == 'delete':
            word_sets.delete()
        elif request.POST.get('submit_action') == 'merge':
            target = word_sets[0]
            for word_set in word_sets[1:]:
                for word in word_set.word_set.all():
                    if not target.word_set.filter(word=word.word, definition=word.definition).exists():
                        word.word_set = target
                        word.save()
                        target.words_number += 1
                word_set.delete()
            target.save()
        else:
            file_content = list()
            for word_set in word_sets:
                file_content.append(u'''Zestaw słówek - {}\n\n'''.format(word_set.title))
                for word in word_set.word_set.all().order_by('-difficulty'):
                    file_content.append(u'''{} - {}\n'''.format(word.word, word.definition))
                file_content.append('\n')
            file_content = ''.join(file_content)
            if request.POST.get('submit_action') == 'download_txt':
                response = HttpResponse(file_content, content_type='text/plain; charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename="words.txt"'
                return response
            elif request.POST.get('submit_action') == 'download_email':
                email = EmailMessage('Zestawy słówek', 'Plik znajduje się w załączniku',
                    EMAIL_HOST_USER, [request.user.email], 
                    attachments=[('words.txt', file_content, 'text/plain; charset=utf-8')])
                email.send()
        redirect(word_sets_list)
    word_sets = request.user.wordset_set.all().order_by('-pub_date')
    return render(request, 'word_sets_list.html', {'word_sets': word_sets})


@login_required
def word_sets_detail(request, pk):
    word_set = request.user.wordset_set.get(pk=pk)
    if request.method == 'POST':
        if request.is_ajax():
            word = word_set.word_set.get(pk=request.POST.get('pk'))
            accessed_attribute = request.POST.get('name') 
            if accessed_attribute == 'word':
                word.word = request.POST.get('value')
                word.save()
            elif accessed_attribute == 'definition':
                word.definition = request.POST.get('value')
                word.save()
            return HttpResponse()
        else:
            words = word_set.word_set.filter(pk__in=request.POST.getlist('word'))
            if request.POST.get('submit_action') == 'delete':
                words.delete()
    word_set = request.user.wordset_set.get(pk=pk)
    words = word_set.word_set.all().order_by('-difficulty')
    return render(request, 'word_sets_detail.html', {'words': words, 'word_set_pk': pk})


@login_required
#@db.transactional(xg=True)
def word_sets_edit(request, pk=None):
    instance = get_object_or_404(WordSet, user=request.user, pk=pk) if pk else None
    edit_mode = True if instance else False
    form = WordSetForm(
        request.POST or None, request.FILES or None,
        instance=instance, user=request.user
    )
    if form.is_valid():
        form.save()
        time.sleep(1)
        return redirect(word_sets_list)
    return render(request, 'word_sets_edit.html', {'form': form, 'edit_mode': edit_mode})
