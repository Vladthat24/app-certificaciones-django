from .base import *

DEBUG = False

CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = INSTALLED_LIBRARIES + INSTALLED_MODULES

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_certificaciones',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
