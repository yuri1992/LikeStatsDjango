from django.conf.urls import patterns, include, url

from .views import stats, login, recount, user, sort_elements_user, make_image
urlpatterns = patterns(
    '',
    url(r'^$', login),
    url(r'^recount/(?P<fb_id>\d+)$', recount),
    url(r'^user/(?P<fb_id>\d+)$', user),
    url(r'^stats/(?P<fb_id>\d+)$', stats),
    url(r'^sort_elements/(?P<fb_id>\d+)$', sort_elements_user),
    url(r'^make_image/+)$', make_image),
)
