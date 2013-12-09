from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template

from djangoappengine.utils import on_production_server, have_appserver
from registration.forms import RegistrationFormUniqueEmail
from registration.backends.default.views import RegistrationView


handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'main.html'}, name='main'),
    url(r'^word_sets/$', 'lingo.views.word_sets_list', name='word_sets_list'),
    url(r'^word_sets/(?P<pk>\d+)/$', 'lingo.views.word_sets_detail', name='word_sets_detail'),
    url(r'^word_sets/edit/$', 'lingo.views.word_sets_edit', name='word_sets_edit'),
    url(r'^word_sets/(?P<pk>\d+)/edit/$', 'lingo.views.word_sets_edit', name='word_sets_edit'),
    url(r'^accounts/login/$', 'lingo.views.login_user'),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormUniqueEmail),
        name='registration_register'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),
    url(r'^accounts/', include('registration.backends.default.urls')),
)

if on_production_server:
    urlpatterns += staticfiles_urlpatterns()
