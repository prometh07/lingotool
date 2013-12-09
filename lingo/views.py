#coding=utf-8
from django.core.mail import EmailMessage
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import WordSetForm, WordSetsListForm, WordSetsDetailForm
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
    form = WordSetsListForm(request.POST or None, user=request.user)
    if form.is_valid():
        if form.submit_action in ('merge', 'delete'):
            form.save()
        elif form.submit_action == 'download_txt':
            file_content = generate_txt_file(form.cleaned_data.get('word_set', None))
            response = HttpResponse(file_content, content_type='text/plain; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="words.txt"'
            return response
        elif form.submit_action == 'download_email':
            file_content = generate_txt_file(form.cleaned_data.get('word_set', None))
            email = EmailMessage('Zestawy słówek', 'Plik znajduje się w załączniku',
                                 EMAIL_HOST_USER, [request.user.email],
                                 attachments=[('words.txt', file_content,
                                               'text/plain; charset=utf-8')])
            email.send()
    if request.method == 'POST':
        return redirect(word_sets_list)
    return render(request, 'word_sets_list.html', {'form': form})


@login_required
def word_sets_detail(request, pk):
    """
    Return details of requested WordSet or modify its contents.
    """
    word_set = get_object_or_404(WordSet, pk=pk, user=request.user)

    if request.method == 'POST' and request.is_ajax():
        if request.POST.get('get_dict_data'):
            word = request.POST.get('word')
            dict_data = get_dictionary_data(word)
            return HttpResponse(dict_data)
        word_set.title = request.POST.get('value')
        word_set.save()
        return HttpResponse()

    form = WordSetsDetailForm(request.POST or None, instance=word_set, user=request.user)
    if form.is_valid():
        if form.submit_action == 'delete':
            form.save()
    if form.submit_action == 'download_txt':
        file_content = generate_txt_file([word_set])
        response = HttpResponse(file_content, content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="words.txt"'
        return response
    elif form.submit_action == 'download_email':
        file_content = generate_txt_file([word_set])
        email = EmailMessage('Zestawy słówek', 'Plik znajduje się w załączniku',
                             EMAIL_HOST_USER, [request.user.email],
                             attachments=[('words.txt', file_content,
                                           'text/plain; charset=utf-8')])
        email.send()

    if request.method == 'POST':
        return redirect(word_sets_detail, pk=pk)
    return render(request, 'word_sets_detail.html',
                  {'word_set_pk': pk, 'word_set_title': word_set.title, 'form': form})


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
    if request.method == 'POST':
        return redirect(word_sets_list)
    return render(request, 'word_sets_edit.html', {'form': form, 'edit_mode': edit_mode})
