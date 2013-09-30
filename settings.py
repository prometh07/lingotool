# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import *
from djangoappengine.utils import on_production_server, have_appserver
import conf
import os
import sys

PROJECT_PATH = os.path.dirname(__file__)

# Activate django-dbindexer for the default database
DATABASES['native'] = DATABASES['default']
DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
AUTOLOAD_SITECONF = 'indexes'

ADMINS = (
    ('Radoslaw Luter', 'lingotool.info@gmail.com'),
)

SECRET_KEY = conf.SECRET_KEY

INSTALLED_APPS = (
#    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'djangotoolbox',
    'autoload',
    'dbindexer',
    'registration',
    'filetransfers',
    'lingo',
    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
)

MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
    'autoload.middleware.AutoloadMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'google.appengine.ext.ndb.django_middleware.NdbDjangoMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

ADMIN_MEDIA_PREFIX = '/media/admin/'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'lingo', 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

STATIC_URL = '/static/'

ROOT_URLCONF = 'urls'
LOGIN_REDIRECT_URL = '/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'TIMEOUT': 0,
    }
}

# django-registration settings
SITE_ID = 1
ACCOUNT_ACTIVATION_DAYS=7
if on_production_server:
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = conf.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = conf.EMAIL_HOST_PASSWORD
    DEFAULT_FROM_EMAIL =  conf.EMAIL_HOST_USER
    SERVER_EMAIL = conf.EMAIL_HOST_USER
else:
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    DEFAULT_FROM_EMAIL = 'webmaster@localhost'

LANGUAGE_CODE = 'pl'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Third party libraries
sys.path.append(os.path.join(PROJECT_PATH, 'lib'))

# Files upload
FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    #'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)
FILE_UPLOAD_TEMP_DIR = os.path.join(PROJECT_PATH, 'tmp')
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440 
