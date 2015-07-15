from celery import Celery
from django.conf import settings
from login.models import Users
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'counter.settings')

app = Celery('tasks',broker='django://')
app.conf.update(BROKER_URL='django://')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    CELERYBEAT_SCHEDULER ='djcelery.schedulers.DatabaseScheduler'
)


@app.task(bind=True)
def fetch_photos_data():
    # user_data = Users.objects.filter(fb_id=fb_id).first()
    return 4 * 4
    # if user_data:
    #     access_token = user_data['access_token']
    #     data = login.facebook_api.GraphAPIHelper.get_user_photos(
    #         fb_id, access_token)
    #     user_data.update_one(photos=data)


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
