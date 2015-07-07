from django.conf.urls import patterns, include, url
from views import Login
urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'counter.views.home', name='home'),
                       url(r'', Login.as_view()),
)
