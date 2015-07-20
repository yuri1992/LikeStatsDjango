from django.views.generic import ListView
from django.shortcuts import render_to_response
from facebook_sdk.facebook_login import FacebookLoginHandler
from facebook_sdk.facebook_helper import GraphAPIHelper
from mongoengine import connect
from models import Users
import tasks
connect('test', host='mongodb://localhost/test')


class Login(ListView):

    def get(self, request):
        res = {}
        login_status = FacebookLoginHandler(request)

        if not login_status.is_login():
            res['redirect_url'] = login_status.get_login_url()
            return render_to_response('login.html', res)
        else:
            res = {}
            Users.objects.reduce_likes()
            GraphAPIHelper.put_wall_post('I am posting...',access_token=login_status.access_token);
            tasks.fetch_all.apply_async([login_status.user_data.fb_id])
            return render_to_response('user.html', res)
