from celery import Celery, chord, group
from django.conf import settings
from login.models import Users
from facebook_sdk.facebook_request import GraphAPIRequest
from facebook_sdk.facebook_helper import GraphAPIHelper
from mongoengine import connect
from datetime import datetime
import os


app = Celery('tasks')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')
app.conf.update(settings.CELERY_CONFIG_MODULE)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


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
    user = Users.objects.filter(fb_id=fb_id).first()
    if user:
        user.update(
            last_time_fetch=datetime.now(),
            fetching_status=True)

        chord(
            group(fetch_photos_data(fb_id),
                  fetch_posts_data(fb_id),
                  fetch_videos_data(fb_id)
                  # fetch_friend_list(fb_id)
                  ),
            group(
                aggregate_likes(fb_id),
                sotring(fb_id))
        )

        user.fetching_status = False
        user.last_finish_fetch = datetime.now()
        user.save()

        tumbnails_creator.apply_async([fb_id])


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


@app.task
def tumbnails_creator(fb_id):
    """
        get user data from DB
        making all nesscery images for facebook sharing
    """
    user = Users.objects.filter(fb_id=fb_id).\
            only('name', 'profile_photo').\
            first()
    if user:
        user = user.to_mongo()
        likes_stats = Likes_Stats.objects.filter(value__fb_id=fb_id).\
            exclude('id', 'value__sorted_videos', 'value__sorted_posts', 'value__sorted_photos').\
            fields(slice__value__top_likers=10).\
            first()
        if likes_stats:
            user['stats'] = likes_stats.to_mongo()['value']
