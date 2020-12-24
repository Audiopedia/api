from .base import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "UpQ792f1jcYJqWapecLom0e5fuCbbFbsOujT3qJAP4pPQD2pOlcQpxvx4Dg6aEGxA10JHfQOZUwS5DVF"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", '.localhost', "21jk0xralk.execute-api.us-east-2.amazonaws.com"]

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
