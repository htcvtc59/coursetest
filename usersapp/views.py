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
from adminapp.models import SubCateCourse, CategoryCourse, Course, \
    EvaluateCommentUsers, Student, UploadFileUsers, Teacher
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
            itemid = dict_keys.get('itemid')
            itemcourse = dict_keys.get('itemcourse')
            teachercourse = dict_keys.get('teachercourse')
            comment = dict_keys.get('comment')

            evaluate = EvaluateCommentUsers.objects.filter(userscomment=itemid, rolecomment=teachercourse,
                                                           coursecomment=itemcourse).first()
            if evaluate:
                evaluate.contentcomment = comment
                evaluate.save()
            else:
                evaluate = EvaluateCommentUsers(userscomment=itemid, rolecomment=teachercourse,
                                                coursecomment=itemcourse, contentcomment=comment)
                evaluate.save()

            return HttpResponse(content="", content_type="application/json", status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def teachergetcomment(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            itemid = dict_keys.get('itemid')
            itemcourse = dict_keys.get('itemcourse')
            teachercourse = dict_keys.get('teachercourse')

            print(itemid, itemcourse, teachercourse)

            evaluate = EvaluateCommentUsers.objects.filter(userscomment=itemid, rolecomment=teachercourse,
                                                           coursecomment=itemcourse).first()
            if evaluate:
                return HttpResponse(content=json.dumps(evaluate.getall()), content_type="application/json", status=200)
            else:
                return HttpResponse(content="", content_type="application/json", status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def teacheruploadfilessub(request):
    try:
        if request.method == 'POST':
            coursecode = request.POST.get('coursecode')
            usersupload = request.POST.get('usersupload')
            name = request.POST.get('name')
            contentfile = request.FILES['contentfile']
            comment = request.POST.get('comment')

            upload = UploadFileUsers(name=name, usersupload=usersupload, coursecode=coursecode,
                                     contentfile=contentfile, comment=comment)
            upload.save()

            return HttpResponse(content=json.dumps(upload.getall()), content_type="application/json", status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def teacherloadsfile(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            itemcourse = dict_keys.get('itemcourse')

            upload = UploadFileUsers.objects.filter(coursecode=itemcourse).order_by("-created")
            resupload = [val.getall() for val in upload]

            return HttpResponse(content=json.dumps(resupload), content_type="application/json",
                                status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def teacherdeletefile(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            pk = dict_keys.get('pk')

            upload = UploadFileUsers.objects.filter(pk=pk).first()
            if upload:
                upload.delete()
                return HttpResponse(content="", content_type="application/json", status=200)
            else:
                return HttpResponse(content="", content_type="application/json", status=404)
    except Exception:
        pass


# student
@ensure_csrf_cookie
def studentgetallcourse(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            perPage = dict_keys.get('perPage')
            currentPage = dict_keys.get('currentPage')
            uid = dict_keys.get('uid')
            studentinfouid = dict_keys.get('studentinfouid')
            offset = (currentPage - 1) * perPage
            datenow = "%02d-%02d-%02d" % (datetime.now().year, datetime.now().month, datetime.now().day)
            rescourse = Course.objects.filter(enddate__gte=datenow, student_id__exact=studentinfouid).order_by(
                '-enddate', '-startdate')[
                        offset:offset + perPage]
            listcourse = [val.getallc() for val in rescourse]
            return HttpResponse(content=json.dumps(listcourse), content_type="application/json", status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def studentgetallcoursecomplete(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            perPage = dict_keys.get('perPage')
            currentPage = dict_keys.get('currentPage')
            uid = dict_keys.get('uid')
            studentinfouid = dict_keys.get('studentinfouid')
            offset = (currentPage - 1) * perPage
            datenow = "%02d-%02d-%02d" % (datetime.now().year, datetime.now().month, datetime.now().day)
            rescourse = Course.objects.filter(enddate__lt=datenow, student_id__exact=studentinfouid).order_by(
                '-enddate', '-startdate')[
                        offset:offset + perPage]
            listcourse = [val.getallc() for val in rescourse]
            return HttpResponse(content=json.dumps(listcourse), content_type="application/json", status=200)
    except Exception:
        pass

def studentcomplete(request):
    try:
        if 'STUDENT' == request.session['role']:
            return render(request, template_name='studentcomplete.html')
    except Exception:
        return render(request, template_name='index.html')
# end student
