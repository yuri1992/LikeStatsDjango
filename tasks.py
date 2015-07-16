from celery import Celery
from django.conf import settings
from login.models import Users
from facebook_sdk.facebook_request import GraphAPIRequest
from facebook_sdk.facebook_helper import GraphAPIHelper
from mongoengine import connect

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'counter.settings')

app = Celery('tasks', broker='django://')
app.conf.update(BROKER_URL='django://')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    CELERYBEAT_SCHEDULER='djcelery.schedulers.DatabaseScheduler'
)


@app.task
def fetch_photos_data(fb_id):
    connect('test', host='mongodb://localhost/test')
    user_data = Users.objects.filter(fb_id=fb_id).first()
    if user_data:
        print user_data.access_token
        data = GraphAPIHelper.get_user_photos(
            fb_id, user_data.access_token)
        return data
    return None


@app.task
def fetch_posts_data(fb_id):
    pass


@app.task
def fetch_videos_data(fb_id):
    pass


@app.task
def fetch_all(fb_id):
    fetch_photos_data(fb_id)
    fetch_posts_data(fb_id)
    fetch_videos_data(fb_id)
