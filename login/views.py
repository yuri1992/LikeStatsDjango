from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loaders.app_directories import app_template_dirs
from django.template import loader, Context
from django.conf import settings
from django.http import JsonResponse
from .models import Users
import facebook_api

GRAPH = facebook_api.GraphAPI()
from mongoengine import connect
connect('test', host='mongodb://localhost/test')

class FacebookLoginHandler(object):

    def __init__(self, request):
        self._request = request

    def _login_with_session(self):
        fb_id = self._request.session.get('fb_id', None)
        access_token = self._request.session.get('access_token', None)

        if fb_id and access_token:
            GRAPH.access_token = access_token
            return GRAPH.validate_access_token()
        return False

    def _login_from_facebook_redirect(self):
        if 'code' in self._request.GET:
            res = self.get_access_token_from_code()
            if 'error' not in res and 'access_token' in res:
                GRAPH.access_token = res['access_token']
                res['user_data'] = GRAPH.request('/me')
                if not Users.objects.find(fb_id=res['user_data']['id']):
                    self.create_user(res)
                else:
                    self.set_login_session(res)
                return True
        return False

    def is_login(self):
        if self._login_with_session():
            return True
        if self._login_from_facebook_redirect():
            return True
        return False

    def get_login_url(self):
        return facebook_api.auth_url(
            settings.FACEBOOK_APP_ID,
            settings.URL_SITE,
            settings.SCOPE_PREMISSON)

    def create_user(self, data):
        Users.objects.create(
            fb_id=data['user_data']['id'],
            email=getattr(data['user_data'], 'email', None),
            first_name=getattr(data['user_data'], 'first_name', None),
            last_name=getattr(data['user_data'], 'last_name', None),
            access_token=getattr(data, 'access_token', None),
            access_token_expires=getattr(data, 'expires', 0),
        )

    def set_login_session(self, res):
        self._request.session['fb_id'] = res['user_data']['id']
        self._request.session['access_token'] = res['access_token']

    def get_access_token_from_code(self):
        return facebook_api.get_access_token_from_code(
            self._request.GET['code'],
            settings.URL_SITE,
            settings.FACEBOOK_APP_ID,
            settings.FACEBOOK_SECRET)


class Login(ListView):

    def get(self, request):
        res = {}
        login_status = FacebookLoginHandler(request)

        if not login_status.is_login():
            res['redirect_url'] = login_status.get_login_url()
            return render_to_response('login.html', res)
        else:
            res = {}
            res['res'] = GRAPH.request('/me')
            res['likes'] = facebook_api.get_user_photos(0, GRAPH.access_token)
            #res['videos'] = facebook_api.get_user_videos(0, GRAPH.access_token)
            #res['posts'] = facebook_api.get_user_posts(0, GRAPH.access_token)

            print res['likes'][0]
            Users.objects.create(photos=res['likes'])

            return render_to_response('user.html', res)


class Mongo(ListView):

    def get(self, request):
        res = Users.objects.all()
        print res
        print res
        return JsonResponse(res,safe=False)
