from __future__ import absolute_import
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from celery import Celery

app = Celery('sna', broker='amqp://', include=['tsa.tasks'])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)

if __name__ == '__main__':
    app.start()