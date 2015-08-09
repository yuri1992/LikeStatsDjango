from .base import *
import sys
import os
from mongoengine import connect


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


URL_SITE = "http://local.ynet.co.il:8080/"

register_mongo_connection(DATABASE_MONGO)
connect(alias='default')