from .base import *

DEBUG = False

# Use Waitress as the production server

# INSTALLED_APPS = ['whitenoise.runserver_nostatic'] + INSTALLED_APPS
# Static files settings
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE


# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('HOST'),
        'PORT': env('PORT'),
    }
}

