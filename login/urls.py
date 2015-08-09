from django.conf.urls import patterns, include, url

from .views import stats, login, recount, user
urlpatterns = patterns(
    '',
    url(r'^$', login),
    url(r'^recount/(?P<fb_id>\d+)$', recount),
    url(r'^user/(?P<fb_id>\d+)$', user),
    url(r'^stats/(?P<fb_id>\d+)$', stats),
)
