from django.conf.urls import patterns, include, url

from .views import stats, login, recount
urlpatterns = patterns(
    '',
    url(r'^$', login),
    url(r'^recount/(?P<fb_id>\d+)$', recount),
    url(r'^stats/(?P<fb_id>\d+)$', stats),
)
