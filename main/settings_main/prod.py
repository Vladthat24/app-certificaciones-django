from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)classification_dropdown %(asctime)classification_dropdown %(module)classification_dropdown %(process)d %(thread)d %(message)classification_dropdown'
        },
        'app': {
            'format': "[%(asctime)classification_dropdown] [%(levelname)classification_dropdown] [%(name)classification_dropdown:%(lineno)classification_dropdown] [%(path)classification_dropdown] [%(ip)classification_dropdown] [%(user)classification_dropdown] %(message)classification_dropdown",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'tracing': {
            'format': "[%(asctime)classification_dropdown] [%(levelname)classification_dropdown] [%(name)classification_dropdown:%(lineno)classification_dropdown] [%(path)classification_dropdown] [%(remote_host)classification_dropdown] [%(server_name)classification_dropdown] [%(language)classification_dropdown] [%(user_agent)classification_dropdown] [%(http_host)classification_dropdown] [%(ip)classification_dropdown] [%(user)classification_dropdown] %(message)classification_dropdown",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'filters': ['require_debug_false']
        },
        'sentry_warning': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'filters': ['require_debug_false']
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['require_debug_true']
        }

    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'access.blacklist': {
            'level': 'WARNING',
            'handlers': ['sentry_warning'],
            'propagate': False,
        },
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['console', 'sentry', ]
    },
}
