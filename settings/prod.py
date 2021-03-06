from .base import *
import sys
import os

BASE_DIR = os.path.join(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(os.path.dirname(__file__))

URL_SITE = "http://howmuchlikesyouworth.com/"
FACEBOOK_SECRET = "c9498587ac9d2a7cee813abbaa8ed7c0"
FACEBOOK_APP_ID = "1649266495305734"

CELERY_CONFIG_MODULE = {
    'BROKER_URL': 'mongodb://localhost:27017/broker',
    'CELERYBEAT_SCHEDULER': 'djcelery.schedulers.DatabaseScheduler',
    'CELERY_RESULT_BACKEND': 'mongodb://localhost:27017/test',
    'CELERY_MONGODB_BACKEND_SETTINGS': {
        'database': 'celery',
        'taskmeta_collection': 'my_taskmeta_collection',
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy'
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

DATABASE_MONGO = {
    'MONGO_HOST': 'mongodb://localhost/test',
    'MONGO_NAME': 'test',
    'MONGO_PORT': '27017',
    'MONGO_MAX_POOL_SIZE': '200',
}


IMAGES = {
    'small': os.path.join(PROJECT_ROOT, 'static/images/small.png'),
    'top_ten': os.path.join(PROJECT_ROOT, 'static/images/top_ten.png'),
}
FONTS = {
    'awesome': os.path.join(PROJECT_ROOT, 'static/css/assets/fonts/fontawesome-webfont.ttf'),
    'dejavu': os.path.join(PROJECT_ROOT, 'static/fonts/arial.ttf'),
}

register_mongo_connection(DATABASE_MONGO)
connect(alias='default')       

