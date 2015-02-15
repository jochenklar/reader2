# coding=utf8
import os

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

SECRET_KEY = 'this is a not very secret key'

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': '',
    #     'USER': '',
    #     'PASSWORD': '',
    #     'HOST': '',
    #     'PORT': '',
    # }

    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': '',
    #     'USER': '',
    #     'PASSWORD': '',
    #     'HOST': '',
    #     'PORT': '',
    # }

    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': '' # path to database file
    # }
}

SITE_ROOT = os.path.dirname(os.path.dirname(__file__))
SITE_URL = 'http://localhost:8000'
