from django.conf.urls import patterns, include, url
from views import Login, Mongo
urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'counter.views.home', name='home'),
                       url(r'all/$', Mongo.as_view()),
                       url(r'', Login.as_view()),
                       )
