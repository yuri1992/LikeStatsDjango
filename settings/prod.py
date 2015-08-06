from .base import *
import sys
import os

BROKER_URL = 'mongodb://localhost/broker',
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_RESULT_BACKEND = 'mongodb://localhost/'
CELERY_MONGODB_BACKEND_SETTINGS = {
    'database': 'celery',
    'taskmeta_collection': 'my_taskmeta_collection',
},

DATABASE_MONGO = {
    'MONGO_HOST': 'mongodb://localhost/test',
    'MONGO_NAME': 'test',
    'MONGO_PORT': '27017',
    'MONGO_MAX_POOL_SIZE': '200',
}

register_mongo_connection(DATABASE_MONGO)
