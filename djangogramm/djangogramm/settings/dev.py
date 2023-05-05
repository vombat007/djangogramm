from .base import *

DEBUG = True

INSTALLED_APPS += ['debug_toolbar', ]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

INTERNAL_IPS = [

    "127.0.0.1",
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
