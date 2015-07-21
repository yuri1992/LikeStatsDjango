from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from facebook_sdk.facebook_login import FacebookLoginHandler
from facebook_sdk.facebook_helper import GraphAPIHelper
from mongoengine import connect
from models import Users, Stats
from bson import ObjectId, Code
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
            res = {
                'fb_id': login_status.user_data.fb_id
            }
            return render_to_response('user.html', res)


class Likes(ListView):

    def get(self, request, fb_id):
        res = {}
        user_data = Users.objects.filter(fb_id=fb_id).first().values_list()
        stats_data = Stats.objects.filter(fb_id=fb_id).first()
        if user_data:
            for x in user_data.photos[:10]:
                print x.__dict__
            res = {
                'fb_id': user_data.fb_id,
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'photos': [x.to_json() for x in user_data.photos[:10]],
                #'posts': user_data.photos[:10],
                #'videos': user_data.photos[:10],
                'stats': {}
            }
        
        return JsonResponse(res, safe=False)
