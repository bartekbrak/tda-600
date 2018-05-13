from .base import *
DEBUG = TOOLBAR = TEMPLATE_DEBUG = False

# speed things up
NOT_TESTED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework.authtoken',
]

INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in NOT_TESTED_APPS]
