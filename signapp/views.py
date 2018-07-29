from django.shortcuts import render
from signapp.models import Account, Role

from django.views.decorators.csrf import ensure_csrf_cookie, requires_csrf_token
from django.http import HttpResponse
from django.core.serializers import serialize
import json
from adminapp.models import Student

from assets.validtoken import *


# Create your views here.

@ensure_csrf_cookie
def signin(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            username = dict_keys.get('username')
            password = dict_keys.get('password')
            account = Account.objects.filter(name=username).first()
            if account and Account.verify_password(account, password) and account.role.name == 'ADMIN':
                res = account._id
                request.session['uid'] = str(res)
                request.session['token'] = createtoken(USERNAME, PASSWORD)
                request.session['role'] = account.role.name
                request.session['username'] = account.info.fullname
                return HttpResponse(content="signed", content_type='application/json', status=200)
            elif account and Account.verify_password(account, password) and account.role.name == 'TEACHER':
                res = account._id
                request.session['uid'] = str(res)
                request.session['token'] = createtoken(USERNAME, PASSWORD)
                request.session['role'] = account.role.name
                request.session['username'] = account.info.fullname
                return HttpResponse(content="signedteacher", content_type='application/json', status=200)
            elif account and Account.verify_password(account, password) and account.role.name == 'STUDENT':
                res = account._id
                request.session['uid'] = str(res)
                request.session['token'] = createtoken(USERNAME, PASSWORD)
                request.session['role'] = account.role.name
                request.session['username'] = account.info.fullname
                # add student info uid
                studentinfouid = Student.objects.filter(accountcode=username).first()
                if studentinfouid:
                    request.session['studentinfouid'] = str(studentinfouid.pk)

                return HttpResponse(content="signedstudent", content_type='application/json', status=200)
            else:
                return HttpResponse(content="", content_type='application/json', status=200)
    except Exception:
        pass
