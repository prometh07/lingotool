from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.auth import views as auth_views


def login_user(request, *args, **kwargs):
    if request.method == 'POST':
        if 'remember_me' in request.POST:
            request.session.set_expiry(604800)
    return auth_views.login(request, *args, **kwargs)


def new_set(request):
    return render_to_response('new_set.html')
