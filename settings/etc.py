# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '8d%r=8-0xc-*l8-r0dm^x##jn$loc_g&o(8*j61%jcs+*)uvs^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

ROOT_URLCONF = 'tsa.urls'

WSGI_APPLICATION = 'tsa.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

CSRF_COOKIE_AGE = 60 * 60  # one hour