# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

# Users applications

INSTALLED_APPS += (
    'tsa',
    'queries',
    'accounts',
    'djcelery'
)