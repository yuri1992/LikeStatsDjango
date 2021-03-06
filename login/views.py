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
from image_maker.api import ImagesMaker
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
        # recount(login_status.user_data.fb_id)
        return render_to_response('user.html', res)


def recount(fb_id):
    # pass
    tasks.fetch_all.apply_async([fb_id])


def make_image(request):
    ImagesMaker.create_small_stat_image({
        'font_icon': unichr(0xF087),
        'title': 'My Total Like',
        'value': '1,000',
        'image_profile': 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xpf1/v/t1.0-1/c113.33.414.414/s50x50/5353_10200578370755373_1977075288_n.jpg?oh=6ed8cec02057e474c1d2139490a39a54&oe=56487D9D&__gda__=1451351050_445fccab167c52b614d93584eb8e601d',
        'file_name' : '1'

    })

    ImagesMaker.create_small_stat_image({
        'font_icon': unichr(0xF031),
        'title': 'Total Likes On Posts',
        'value': '1,000',
        'image_profile': 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xpf1/v/t1.0-1/c113.33.414.414/s50x50/5353_10200578370755373_1977075288_n.jpg?oh=6ed8cec02057e474c1d2139490a39a54&oe=56487D9D&__gda__=1451351050_445fccab167c52b614d93584eb8e601d',
        'file_name' : '2'

    })
    return HttpResponse("<img src='/static/images/1.png'><img src='/static/images/2.png'>")


def sort_elements_user(request, fb_id):
    res = Users.objects.\
        filter(fb_id=fb_id).\
        sort_elements()
    return JsonResponse(res, encoder=JsonMongodbEncoder, safe=False)


def user(request, fb_id):
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
            fields(slice__photos=5).\
            fields(slice__posts=5).\
            fields(slice__videos=5).\
            only('name', 'link', 'fetching_status', 'photos', 'videos', 'posts', 'profile_photo', 'cover').\
            first()

        if res:
            res = res.to_mongo()
        else:
            return JsonResponse({})

        likes_stats = Likes_Stats.objects.filter(value__fb_id=fb_id).\
            exclude('id').\
            fields(slice__value__top_likers=10).\
            fields(slice__value__sorted_videos=5).\
            fields(slice__value__sorted_posts=5).\
            fields(slice__value__sorted_photos=5).\
            first()
        if likes_stats:
            res['stats'] = likes_stats.to_mongo()['value']

        return JsonResponse(res, encoder=JsonMongodbEncoder, safe=False)
    return JsonResponse({})
