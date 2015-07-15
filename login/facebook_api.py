from django.conf import settings
from .models import Users
import tasks

import hashlib
import hmac
import base64
import requests
import json
import re




class GraphAPIHelper(object):

    @classmethod
    def get_connections(cls, id, connection_name, **args):
        """Fetchs the connections for given object."""
        return self.request(
            setting.FACEBOOK_VERSION + "/" + id + "/" + connection_name, args)

    def put_object(self, parent_object, connection_name, **data):
        """Writes the given object to the graph, connected to the given parent.

        For example,

            graph.put_object("me", "feed", message="Hello, world")

        writes "Hello, world" to the active user's wall. Likewise, this
        will comment on a the first post of the active user's feed:

            feed = graph.get_connections("me", "feed")
            post = feed["data"][0]
            graph.put_object(post["id"], "comments", message="First!")

        See http://developers.facebook.com/docs/api#publishing for all
        of the supported writeable objects.

        Certain write operations require extended permissions. For
        example, publishing to a user's feed requires the
        "publish_actions" permission. See
        http://developers.facebook.com/docs/publishing/ for details
        about publishing permissions.

        """
        assert self.access_token, "Write operations require an access token"
        return self.request(
            self.version + "/" + parent_object + "/" + connection_name,
            post_args=data,
            method="POST")

    def put_wall_post(self, message, attachment={}, profile_id="me"):
        """Writes a wall post to the given profile's wall.

        We default to writing to the authenticated user's wall if no
        profile_id is specified.

        attachment adds a structured attachment to the status message
        being posted to the Wall. It should be a dictionary of the form:

            {"name": "Link name"
             "link": "http://www.example.com/",
             "caption": "{*actor*} posted a new review",
             "description": "This is a longer description of the attachment",
             "picture": "http://www.example.com/thumbnail.jpg"}

        """
        return self.put_object(profile_id, "feed", message=message,
                               **attachment)

    def get_app_access_token(self, app_id, app_secret):
        """Get the application's access token as a string."""
        args = {'grant_type': 'client_credentials',
                'client_id': app_id,
                'client_secret': app_secret}

        return self.request("oauth/access_token", args=args)["access_token"]

    @classmethod
    def get_access_token_from_code(
            self, code, redirect_uri, app_id, app_secret):
        """Get an access token from the "code" returned from an OAuth dialog.

        Returns a dict containing the user-specific access token and its
        expiration date (if applicable).

        """
        args = {
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": app_id,
            "client_secret": app_secret}

        return GraphRequest.request(None, "oauth/access_token", args)

    def extend_access_token(self, app_id, app_secret):
        """
        Extends the expiration time of a valid OAuth access token. See
        <https://developers.facebook.com/roadmap/offline-access-removal/
        # extend_token>

        """
        args = {
            "client_id": app_id,
            "client_secret": app_secret,
            "grant_type": "fb_exchange_token",
            "fb_exchange_token": self.access_token,
        }

        return self.request("oauth/access_token", args=args)

    @classmethod
    def validate_access_token(cls, access_token):
        """
            Validate access token with Graph API
        """
        params = {
            'input_token': access_token
        }

        res = GraphRequest.request(
            access_token,
            '/debug_token',
            args=params
        )

        if 'is_valid' in res['data']:
            return bool(res['data']['is_valid'])
        return False

    @classmethod
    def get_user_photos(cls, fb_id, access_token):
        """
            return all user photos by access_token
        """
        args = {
            'fields': 'likes.summary(true){pic_small,name,id,can_post},picture,name'}
        res = GraphRequest(access_token, '/me/photos', args).get_all()
        return res

    def get_user_videos(fb_id, access_token):
        """
            return all user photos by access_token
        """
        args = {
            'fields': 'likes.summary(true){pic_small,name,id,can_post},picture,name'}
        res = GraphRequest(access_token, '/me/videos', args).get_all()
        return res

    def get_user_posts(fb_id, access_token):
        """
            return all user photos by access_token
        """
        args = {
            'fields': 'likes.summary(true){pic_small,name,id,can_post},picture,name'}
        res = GraphRequest(access_token, '/me/posts', args).get_all()
        return res

    @classmethod
    def auth_url(cls, app_id, canvas_url, perms=None, **kwargs):
        url = "https://www.facebook.com/dialog/oauth?"
        kvps = {'client_id': app_id, 'redirect_uri': canvas_url}
        if perms:
            kvps['scope'] = ",".join(perms)
        kvps.update(kwargs)
        return url + urlencode(kvps)

    def get_app_access_token(app_id, app_secret):
        return get_app_access_token(app_id, app_secret)



class FacebookLoginHandler(object):

    def __init__(self, request):
        self._request = request

    def _login_with_session(self):
        fb_id = self._request.session.get('fb_id', None)
        access_token = self._request.session.get('access_token', None)

        if fb_id and access_token and self.user_exsits(fb_id):
            tasks.fetch_photos_data(fb_id)
            return GraphAPIHelper.validate_access_token(access_token)
        return False

    def _login_from_facebook_redirect(self):
        if 'code' in self._request.GET:
            res = self.get_access_token_from_code()
            if 'error' not in res and 'access_token' in res:
                access_token = res['access_token']
                res['user_data'] = GraphRequest.request(access_token,
                    '/me')
                if not Users.objects.filter(fb_id=res['user_data']['id']):
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

    def user_exsits(self, fb_id):
        if Users.objects.filter(fb_id=fb_id).first():
            return True
        return False

    def get_login_url(self):
        return GraphAPIHelper.auth_url(
            settings.FACEBOOK_APP_ID,
            settings.URL_SITE,
            settings.SCOPE_PREMISSON)

    def create_user(self, data):
        fb_id = data['user_data']['id']
        del data['user_data']['id']

        self.register_tasks_on_new_user(fb_id)
        Users.objects.create(
            fb_id=fb_id,
            access_token=getattr(data, 'access_token', None),
            access_token_expires=getattr(data, 'expires', 0),
            **data['user_data']
        )

    def register_tasks_on_new_user(self, fb_id):
        tasks.fetch_photos_data(fb_id)
        # register more tasks

    def set_login_session(self, res):
        self._request.session['fb_id'] = res['user_data']['id']
        self._request.session['access_token'] = res['access_token']

    def get_access_token_from_code(self):
        return GraphAPIHelper.get_access_token_from_code(
            self._request.GET['code'],
            settings.URL_SITE,
            settings.FACEBOOK_APP_ID,
            settings.FACEBOOK_SECRET)
