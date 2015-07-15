from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import loader, Context
from django.conf import settings
from django.http import JsonResponse
from .models import Users
from .facebook_api import FacebookLoginHandler
from mongoengine import connect
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
            return render_to_response('user.html', res)