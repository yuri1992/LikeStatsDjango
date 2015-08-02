from django.conf.urls import patterns, include, url

from .views import stats, login
urlpatterns = patterns(
    '',
    url(r'^$', login),
    url(r'^stats/(?P<fb_id>\d+)$', stats),
)
