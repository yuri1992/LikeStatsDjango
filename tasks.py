from celery import Celery, chord, group
from django.conf import settings
from login.models import Users
from facebook_sdk.facebook_request import GraphAPIRequest
from facebook_sdk.facebook_helper import GraphAPIHelper
from mongoengine import connect
import os


app = Celery('tasks')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
app.conf.update(settings.CELERY_CONFIG_MODULE)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

print app.conf.CELERY_RESULT_BACKEND

@app.task
def fetch_photos_data(fb_id):
    connect(alias='default')
    user_data = Users.objects.filter(fb_id=fb_id).first()
    if user_data:
        data = GraphAPIHelper.get_user_photos(
            fb_id, user_data.access_token)
        user_data.update(photos=data)
        return data
    return None


@app.task
def fetch_posts_data(fb_id):
    connect(alias='default')
    user_data = Users.objects.filter(fb_id=fb_id).first()
    if user_data:
        data = GraphAPIHelper.get_user_posts(
            fb_id, user_data.access_token)
        user_data.update(posts=data)
        return data
    return None


@app.task
def fetch_videos_data(fb_id):
    connect(alias='default')
    user_data = Users.objects.filter(fb_id=fb_id).first()
    if user_data:
        data = GraphAPIHelper.get_user_videos(
            fb_id, user_data.access_token)
        user_data.update(videos=data)
        return data
    return None


@app.task
def fetch_friend_list(fb_id):
    connect(alias='default')
    user_data = Users.objects.filter(fb_id=fb_id).first()
    if user_data:
        data = GraphAPIHelper.get_user_friends(
            fb_id, user_data.access_token)
        user_data.update(friends=data)
        return data
    return None


@app.task
def fetch_all(fb_id):
    chord(
        group(fetch_photos_data(fb_id),
              fetch_posts_data(fb_id),
              fetch_videos_data(fb_id)
              # fetch_friend_list(fb_id)
              ),
        group(
            sotring(fb_id),
            aggregate_likes(fb_id))
    )


@app.task
def aggregate_likes(fb_id):
    if isinstance(fb_id, int):
        fb_id_list = [fb_id]
    users = Users.objects.filter(fb_id=fb_id)
    users.reduce_likes()


@app.task
def sotring(fb_id):
    if isinstance(fb_id, int):
        fb_id_list = [fb_id]
    users = Users.objects.filter(fb_id=fb_id)
    users.sort_elements()
