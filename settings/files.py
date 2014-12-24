from etc import BASE_DIR, os

STATIC_URL = '/static/'
MEDIA_URL = '/media/'


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)