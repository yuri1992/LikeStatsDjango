from __future__ import absolute_import
from celery import Celery
from django.conf import settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'counter.settings')

from django.conf import settings

app = Celery('proj')
app.conf.update(
    BROKER_URL='django://'
)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task
def count(self):
    return (2 * 2 * 2 * 2)

