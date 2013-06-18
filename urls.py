from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
handler500 = 'djangotoolbox.errorviews.server_error'


urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'main.html'}, name='main'),
    url(r'^new_set/$', 'lingo.views.new_set', name='new_set'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', 
        {'next_page': '/', 'template_name': 'main.html'}, name='logout'),
    url(r'^accounts/register/$', 'lingo.views.register', name='register'),
    url(r'^accounts/profile/$', direct_to_template, {'template': 'main.html'}, name='profile'),
)
urlpatterns += staticfiles_urlpatterns()


