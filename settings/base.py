"""
Django settings for counter project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from mongoengine import register_connection

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8x0xa(6jz8pef9_d7%b35dr3#6@f3rq1hs)4wnx0_5g&-2841a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    PROJECT_ROOT + '/templates/',
)




SCOPE_PREMISSON = [
    'user_likes',
    'user_photos',
    'user_status',
    'user_videos',
    'user_posts',
    'publish_actions'
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
    'djcelery'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases




# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
APP_DIRS = True

URL_SITE = "http://local.ynet.co.il:8080/"
FACEBOOK_SECRET = "c9498587ac9d2a7cee813abbaa8ed7c0"
FACEBOOK_APP_ID = "1649266495305734"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


USER_PROFILES_FIEDLS='id,name,cover,gender,location,locale,link,picture'

def register_mongo_connection(db):
    register_connection(
        'default',
        name=db['MONGO_NAME'],
        host=db['MONGO_HOST'],
        port=db['MONGO_PORT'],
        **{
            'maxPoolSize': db['MONGO_MAX_POOL_SIZE'],
        }
    )
