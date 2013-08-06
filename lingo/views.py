from django.shortcuts import render, get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from lingo.models import Word, WordSet
from lingo.forms import WordSetForm
from google.appengine.ext import db
import time

def login_user(request, *args, **kwargs):
    if request.POST.get('remember_me'):
        request.session.set_expiry(604800)
    return auth_views.login(request, *args, **kwargs)


@login_required
def word_sets_list(request):
    word_sets = request.user.wordset_set.all().order_by('-pub_date')
    return render(request, 'word_sets_list.html', {'word_sets': word_sets})


@login_required
def word_sets_detail(request, pk):
    word_set = get_object_or_404(WordSet, pk=pk)
    words = word_set.word_set.all().order_by('-difficulty')
    return render(request, 'word_sets_detail.html', {'words': words})


@login_required
#@db.transactional(xg=True)
def word_sets_edit(request, pk=None):
    instance = get_object_or_404(WordSet, user=request.user, pk=pk) if pk else None
    edit_mode = True if instance else False
    form = WordSetForm(request.POST or None, request.FILES or None, 
        instance=instance, user=request.user)
    if form.is_valid():
        form.save()
        time.sleep(1)
        #return HttpResponseRedirect('/word_sets/{}/'.format(word_set.id))
        return HttpResponseRedirect('/word_sets/')
    return render(request, 'word_sets_edit.html', {'form': form, 'edit_mode': edit_mode})


@login_required
def word_sets_delete(request):
    pass


@login_required
def delete_word(request):
    pass
