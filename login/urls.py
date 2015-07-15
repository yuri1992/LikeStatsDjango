from django.conf.urls import patterns, include, url
<<<<<<< HEAD
from .views import Login
urlpatterns = patterns(
    '',
    url(r'', Login.as_view()),
)
=======
from views import Login, Mongo
urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'counter.views.home', name='home'),
                       url(r'all/$', Mongo.as_view()),
                       url(r'', Login.as_view()),
                       )
>>>>>>> bdc7b87baa7c871d8ddc960065d07edba733ddc0
