from django.conf import settings
from login.models import Users
from .facebook_request import GraphAPIRequest
from .facebook_helper import GraphAPIHelper
import tasks


class FacebookLoginHandler(object):

    def __init__(self, request):
        self._request = request

    def is_login(self):
        if self._login_with_session():
            return True
        if self._login_from_facebook_redirect():
            return True
        return False

    def _login_with_session(self):
        fb_id = self._request.session.get('fb_id', None)
        access_token = self._request.session.get('access_token', None)

        if fb_id and access_token and self._user_exsits(fb_id):
            return GraphAPIHelper.validate_access_token(access_token)
        return False

    def _login_from_facebook_redirect(self):
        if 'code' in self._request.GET:
            code = self._request.GET['code']
            res = self.get_access_token_from_code(code)
            if 'error' not in res and 'access_token' in res:
                access_token = res['access_token']
                res['user_data'] = GraphAPIRequest(
                    access_token, '/me').get().response

                if not Users.objects.filter(fb_id=res['user_data']['id']):
                    self.on_new_user(res)
                self._set_login_session(res)
                return True
        return False

    def on_new_user(self, data):
        self._create_user(data)
        self._register_tasks(data)

    def _create_user(self, data):
        fb_id = data['user_data']['id']
        del data['user_data']['id']
        Users.objects.create(
            fb_id=fb_id,
            access_token=getattr(data, 'access_token', None),
            access_token_expires=getattr(data, 'expires', 0),
            **data['user_data']
        )

    def _user_exsits(self, fb_id):
        if Users.objects.filter(fb_id=fb_id).first():
            return True
        return False

    def _register_tasks(self, data):
        tasks.fetch_all(data['user_data']['id'])

    def _set_login_session(self, res):
        self._request.session['fb_id'] = res['user_data']['id']
        self._request.session['access_token'] = res['access_token']

    @staticmethod
    def get_access_token_from_code(code, redirect_uri=settings.URL_SITE,
                                   app_id=settings.FACEBOOK_APP_ID,
                                   app_secret=settings.FACEBOOK_SECRET):
        args = {
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": app_id,
            "client_secret": app_secret}

        return GraphAPIRequest(None, "oauth/access_token", args).get().response

    @staticmethod
    def get_login_url():
        url = "https://www.facebook.com/dialog/oauth?"
        kvps = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': settings.URL_SITE,
        }
        if perms:
            kvps['scope'] = ",".join(settings.SCOPE_PREMISSON)
        kvps.update(kwargs)
        return url + urlencode(kvps)
