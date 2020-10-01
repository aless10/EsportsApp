from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DEV_SECRET_KEY")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("DEV_DB_NAME"),
        'USER': os.environ.get("DEV_DB_USER"),
        'PASSWORD': os.environ.get("DEV_DB_PASSWORD"),
        'HOST': os.environ.get("DEV_DB_HOST"),
        'PORT': os.environ.get("DEV_DB_PORT", 5432)
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
