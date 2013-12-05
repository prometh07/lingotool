#coding=utf-8
from django.core.mail import EmailMessage
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import WordSetForm
from .helpers import generate_txt_file, get_dictionary_data
from .models import Word, WordSet
from conf import EMAIL_HOST_USER


def login_user(request, *args, **kwargs):
    """
    Login the user.
    """
    if request.POST.get('remember_me'):
        request.session.set_expiry(604800)
    return auth_views.login(request, *args, **kwargs)


@login_required
def word_sets_list(request):
    """
    Return the list of WordSets belonging to the user or modify some of them.
    """
    if request.method == 'POST':
        word_sets = request.user.wordset_set.filter(pk__in=request.POST.getlist('word_set'))
        if request.POST.get('submit_action') == 'delete':
            word_sets.delete()
        elif request.POST.get('submit_action') == 'merge':
            target = word_sets[0]
            target.merge(word_sets[1:])
        elif request.POST.get('submit_action') == 'download_txt':
            file_content = generate_txt_file(word_sets)
            response = HttpResponse(file_content, content_type='text/plain; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="words.txt"'
            return response
        elif request.POST.get('submit_action') == 'download_email':
            file_content = generate_txt_file(word_sets)
            email = EmailMessage('Zestawy słówek', 'Plik znajduje się w załączniku',
                                 EMAIL_HOST_USER, [request.user.email],
                                 attachments=[('words.txt', file_content,
                                               'text/plain; charset=utf-8')])
            email.send()
        return redirect(word_sets_list)

    word_sets = request.user.wordset_set.all().order_by('-pub_date')
    return render(request, 'word_sets_list.html', {'word_sets': word_sets})


@login_required
def word_sets_detail(request, pk):
    """
    Return details of requested WordSet or modify its contents.
    """
    word_set = get_object_or_404(WordSet, pk=pk, user=request.user)

    if request.method == 'POST':
        if request.is_ajax():
            if request.POST.get('get_dict_data'):
                word_id = request.POST.get('word_id')
                dict_data = get_dictionary_data(word)
                return HttpResponse(dict_data)
            attribute = request.POST.get('name')
            if attribute == 'title':
                word_set.title = request.POST.get('value')
                word_set.save()
            else:
                word = get_object_or_404(Word, word_set=word_set, pk=request.POST.get('pk'))
                if attribute == 'word':
                    word.word = request.POST.get('value')
                    word.save()
                elif attribute == 'definition':
                    word.definition = request.POST.get('value')
                    word.save()
            return HttpResponse()

        words = word_set.word_set.filter(pk__in=request.POST.getlist('word'))
        if request.POST.get('submit_action') == 'delete':
            words.delete()
        else:
            file_content = generate_txt_file([word_set])
            if request.POST.get('submit_action') == 'download_txt':
                response = HttpResponse(file_content, content_type='text/plain; charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename="words.txt"'
                return response
            elif request.POST.get('submit_action') == 'download_email':
                email = EmailMessage('Zestawy słówek', 'Plik znajduje się w załączniku',
                                     EMAIL_HOST_USER, [request.user.email],
                                     attachments=[('words.txt', file_content,
                                                   'text/plain; charset=utf-8')])
                email.send()
        return redirect(word_sets_detail, pk=pk)

    words = word_set.word_set.all().order_by('-difficulty')
    return render(request, 'word_sets_detail.html',
                  {'words': words, 'word_set_pk': pk, 'word_set_title': word_set.title})


@login_required
def word_sets_edit(request, pk=None):
    """
    Modify exisiting WordSet or create a new one.
    """
    word_set = get_object_or_404(WordSet, pk=pk, user=request.user) if pk else None
    edit_mode = True if word_set else False
    form = WordSetForm(request.POST or None, request.FILES or None,
                       instance=word_set, user=request.user)
    if form.is_valid():
        form.save()
        if edit_mode:
            return redirect(word_sets_detail, pk=pk)
        redirect(word_sets_list)
    return render(request, 'word_sets_edit.html', {'form': form, 'edit_mode': edit_mode})
