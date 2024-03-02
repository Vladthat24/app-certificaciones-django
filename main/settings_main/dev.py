from .base import *

DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = INSTALLED_LIBRARIES + INSTALLED_MODULES

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'diris_certificaciones',
        'USER': 'root',
        'PASSWORD': 'Administrador@123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
