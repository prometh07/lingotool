from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
from registration.forms import RegistrationFormUniqueEmail
from registration.backends.default.views import RegistrationView
handler500 = 'djangotoolbox.errorviews.server_error'


urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'main.html'}, name='main'),
    url(r'^accounts/login/$', 'lingo.views.login_user'),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormUniqueEmail),
        name='registration_register'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^new_set/$', 'lingo.views.new_set', name='new_set'),
)
urlpatterns += staticfiles_urlpatterns()


