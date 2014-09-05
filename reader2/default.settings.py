import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'not secret'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['reader.jochenklar.de']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'feeds'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'reader2.urls'

WSGI_APPLICATION = 'reader2.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'reader',
        'USER': 'reader'
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR,'static/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'reader2/static/'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'reader2/templates/'),
)