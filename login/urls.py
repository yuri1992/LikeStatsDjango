from django.conf.urls import patterns, include, url

from .views import Login
urlpatterns = patterns(
    '',
    url(r'', Login.as_view()),
)
