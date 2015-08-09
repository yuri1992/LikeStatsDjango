from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, requires_csrf_token
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from facebook_sdk.facebook_login import FacebookLoginHandler
from facebook_sdk.facebook_helper import GraphAPIHelper
from mongoengine import connect
from models import Users, Stats, Likes_Stats
from bson import ObjectId, Code
from django.core.serializers.json import DjangoJSONEncoder
import tasks
import json
import datetime

connect(alias='default')


class JsonMongodbEncoder(DjangoJSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return o.strftime('%d/%m/%y %H:%M:%S')
        return super(JsonMongodbEncoder, self).defualt(o)


@requires_csrf_token
def login(request):
    res = {}
    login_status = FacebookLoginHandler(request)

    if not login_status.is_login():
        res['redirect_url'] = login_status.get_login_url()
        return render_to_response('login.html', res)
    else:
        res = csrf(request)
        res.update({
            'fb_id': login_status.user_data.fb_id,
        })
        recount(login_status.user_data.fb_id)
        return render_to_response('user.html', res)


def recount(fb_id):
    tasks.fetch_all.apply_async([fb_id])



def user(request,fb_id):
    res = Users.objects.\
            filter(fb_id=fb_id).\
            exclude('access_token').\
            fields(slice__photos=1).\
            fields(slice__posts=1).\
            fields(slice__videos=1).\
            first()
    if res:
        res = res.to_mongo()
    else:
        return JsonResponse({})
    return JsonResponse(res, encoder=JsonMongodbEncoder, safe=False)



def stats(request, fb_id):
    if request.META['REQUEST_METHOD'] == 'POST' or 1 == 1:
        res = {}
        res = Users.objects.\
            filter(fb_id=fb_id).\
            exclude('access_token').\
            fields(slice__photos=10).\
            fields(slice__posts=10).\
            fields(slice__videos=10).\
            only('name', 'link','fetching_status','photos', 'videos', 'posts','profile_photo','cover').\
            first()

        if res:
            res = res.to_mongo()
        else:
            return JsonResponse({})

        likes_stats = Likes_Stats.objects.filter(value__fb_id=fb_id).\
            exclude('id').\
            fields(slice__value__top_likers=10).\
            first()
        if likes_stats:
            res['stats'] = likes_stats.to_mongo()['value']

        return JsonResponse(res, encoder=JsonMongodbEncoder, safe=False)
    return JsonResponse({})
