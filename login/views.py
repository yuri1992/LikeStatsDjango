from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from facebook_sdk.facebook_login import FacebookLoginHandler
from facebook_sdk.facebook_helper import GraphAPIHelper
from mongoengine import connect
from models import Users, Stats
from bson import ObjectId, Code
from django.core.serializers.json import DjangoJSONEncoder
import tasks
import json
connect('test', host='mongodb://localhost/test')


class JsonMongodbEncoder(DjangoJSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super(JsonMongodbEncoder, self).defualt(o)


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
        res = Users.objects.\
            filter(fb_id=fb_id).\
            exclude('access_token').\
            fields(slice__photos=10).\
            fields(slice__posts=10).\
            fields(slice__videos=10).\
            first().\
            to_mongo()

        # print user_data
        # print dir(user_data)
        # stats_data = Stats.objects.filter(fb_id=fb_id).first()
        # if user_data:
        #     for x in user_data[0].photos[:10]:
        #         print x.__dict__
        #     res = {
        #         'fb_id': user_data.fb_id,
        #         'first_name': user_data.first_name,
        #         'last_name': user_data.last_name,
        #         'photos': [x.to_json() for x in user_data.photos[:10]],
        # 'posts': user_data.photos[:10],
        # 'videos': user_data.photos[:10],
        #         'stats': {}
        #     }

        return JsonResponse(res, encoder=JsonMongodbEncoder, safe=False)
