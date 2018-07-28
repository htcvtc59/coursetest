from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from assets.validtoken import *
from adminapp.models import Course
from signapp.models import Account, Role, InfoTeacher
import json
from django.core.serializers import serialize
import requests
from django.core.files.storage import FileSystemStorage
import os
import base64
import sys
from django.core.files.base import ContentFile
from datetime import datetime
from django.conf import settings

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from passlib.apps import custom_app_context as pwd_context
from adminapp.models import SubCateCourse, CategoryCourse, Course, Student, UploadFileUsers, Teacher
import math


# Create your views here.

def usersappsignin(request):
    try:
        if 'signout' == request.session['uid'] or not request.session['uid'] or not request.session['role']:
            return render(request, template_name='index.html')
        elif 'TEACHER' == request.session['role']:
            return render(request, template_name='usersappmainteacher.html')
        elif 'STUDENT' == request.session['role']:
            return render(request, template_name='usersappmainstudent.html')
    except Exception:
        return render(request, template_name='index.html')


@ensure_csrf_cookie
def teachergetallcourse(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            perPage = dict_keys.get('perPage')
            currentPage = dict_keys.get('currentPage')
            uid = dict_keys.get('uid')
            offset = (currentPage - 1) * perPage

            datenow = "%02d-%02d-%02d" % (datetime.now().year, datetime.now().month, datetime.now().day)
            rescourse = Course.objects.filter(enddate__gte=datenow, startdate__lt=datenow).order_by('-enddate',
                                                                                                    '-startdate')[
                        offset:offset + perPage]
            listcourse = []
            for val in rescourse:
                account = dict(val.teacher.getall())['account']
                if account == uid:
                    listcourse.append(val.getallc())

            return HttpResponse(content=json.dumps(listcourse), content_type="application/json", status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def teachercommentperstudent(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
    except Exception:
        pass