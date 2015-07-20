from celery import Celery
from django.conf import settings
from login.models import Users
from facebook_sdk.facebook_request import GraphAPIRequest
from facebook_sdk.facebook_helper import GraphAPIHelper
from mongoengine import connect
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'counter.settings')

app = Celery('tasks', broker_url='mongodb://localhost/broker')

app.config_from_object('django.conf:settings')
app.conf.update(
    BROKER_URL='mongodb://localhost/broker',
    CELERYBEAT_SCHEDULER='djcelery.schedulers.DatabaseScheduler',
    CELERY_RESULT_BACKEND='mongodb://localhost/',
    CELERY_MONGODB_BACKEND_SETTINGS={
        'database': 'celery',
        'taskmeta_collection': 'my_taskmeta_collection',
    },

)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def fetch_photos_data(fb_id):
    connect('test', host='mongodb://localhost/test')
    user_data = Users.objects.filter(fb_id=fb_id).first()
    if user_data:
        data = GraphAPIHelper.get_user_photos(
            fb_id, user_data.access_token)
        user_data.update(photos=data)
        return data
    return None


@app.task
def fetch_posts_data(fb_id):
    connect('test', host='mongodb://localhost/test')
    user_data = Users.objects.filter(fb_id=fb_id).first()
    if user_data:
        data = GraphAPIHelper.get_user_posts(
            fb_id, user_data.access_token)
        user_data.update(posts=data)
        return data
    return None


@app.task
def fetch_videos_data(fb_id):
    connect('test', host='mongodb://localhost/test')
    user_data = Users.objects.filter(fb_id=fb_id).first()
    if user_data:
        data = GraphAPIHelper.get_user_videos(
            fb_id, user_data.access_token)
        user_data.update(videos=data)
        return data
    return None

@app.task
def fetch_friend_list(fb_id):
    connect('test', host='mongodb://localhost/test')
    user_data = Users.objects.filter(fb_id=fb_id).first()
    if user_data:
        data = GraphAPIHelper.get_user_friends(
            fb_id, user_data.access_token)
        user_data.update(friends=data)
        return data
    return None

@app.task
def fetch_all(fb_id):
    fetch_photos_data(fb_id)
    fetch_posts_data(fb_id)
    fetch_videos_data(fb_id)
    fetch_friend_list(fb_id)
    sotring(fb_id)
    aggregate_likes(fb_id)


@app.task
def aggregate_likes(fb_id_list):
    if isinstance(fb_id_list, int):
        fb_id_list = [fb_id_list]
    users = Users.objects.filter(fb_id__in=fb_id_list)
    users.reduce_likes()

@app.task
def sotring(fb_id_list):
    if isinstance(fb_id_list, int):
        fb_id_list = [fb_id_list]
    users = Users.objects.filter(fb_id__in=fb_id_list)
    users.sort_elements()
