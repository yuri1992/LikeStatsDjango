from django.conf.urls import patterns, include, url

from .views import Login, Likes
urlpatterns = patterns(
    '',
    url(r'^$', Login.as_view()),
    url(r'^stats/(?P<fb_id>\d+)$', Likes.as_view()),
)
