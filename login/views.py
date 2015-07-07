from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loaders.app_directories import app_template_dirs
from django.template import loader, Context
from django.conf import settings
from .models import User
import facebook_api


class FacebookLoginHandler(object):

    def __init__(self, request):
        self._request = request
        self._graph = facebook_api.GraphAPI()

    def _login_throw_session(self):
        return False

    def _login_from_facebook_redirect(self):
        if 'code' in self._request.GET:
            res = facebook_api.get_access_token_from_code(
                self._request.GET['code'],
                settings.URL_SITE,
                settings.FACEBOOK_APP_ID,
                settings.FACEBOOK_SECRET)
            if 'error' not in res:
                self._graph.access_token = res['access_token']
                res['user_data'] = self._graph.request('/me')
                if not User.objects.user_exists(res['user_data']['id']):
                    print res
                    self.create_user(res)
                return True
        return False

    def is_login(self):
        if self._login_throw_session():
            return True
        if not self._login_from_facebook_redirect():
            return True
        return False

    def get_login_url(self):
        return facebook_api.auth_url(
            settings.FACEBOOK_APP_ID,
            settings.URL_SITE,
            settings.SCOPE_PREMISSON)

    def create_user(self, data):
        print data['user_data']
        User.objects.create(
            fb_id=data['user_data']['id'],
            email=getattr(data['user_data'], 'email', None),
            first_name=getattr(data['user_data'], 'first_name', None),
            last_name=getattr(data['user_data'], 'last_name', None),
            access_token=getattr(data, 'access_token', None),
            access_token_expires=getattr(data, 'expires', 0),
        )


class Login(ListView):

    def get(self, request):
        res = {}
        login_status = FacebookLoginHandler(request)

        if login_status.is_login():
            res['redirect_url'] = login_status.get_login_url()
            return render_to_response('login.html', res)
        else:
            return render_to_response('user.html', res)
