<<<<<<< HEAD
=======
from __future__ import absolute_import
>>>>>>> bdc7b87baa7c871d8ddc960065d07edba733ddc0
from celery import Celery
from django.conf import settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'counter.settings')
<<<<<<< HEAD
from django.conf import settings
from login.models import Users
import login.facebook_api

app = Celery('proj')
app.conf.update(BROKER_URL='django://')
=======

from django.conf import settings

app = Celery('proj')
app.conf.update(
    BROKER_URL='django://'
)

>>>>>>> bdc7b87baa7c871d8ddc960065d07edba733ddc0
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


<<<<<<< HEAD
@app.task
def fetch_photos_data(fb_id):
    user_data = Users.objects.filter(fb_id=fb_id).first()
    if user_data:
        access_token = user_data['access_token']
        data = login.facebook_api.GraphAPIHelper.get_user_photos(fb_id, access_token)
        print data
        user_data.update_one(photos=data)



@app.task
def fetch_posts_data(fb_id):
    pass


@app.task
def fetch_videos_data(fb_id):
    pass


@app.task
def fetch_all(fb_id):
    pass
=======
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task
def count(self):
    return (2 * 2 * 2 * 2)

>>>>>>> bdc7b87baa7c871d8ddc960065d07edba733ddc0
