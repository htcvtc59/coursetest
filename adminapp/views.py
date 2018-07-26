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
from adminapp.models import SubCateCourse, CategoryCourse, Course, Student, CommentUsers, UploadFileUsers, Teacher
import math

# Create your views here.

headers = {
    "Content-Type": "application/json"
}


def adminbasecourse(request):
    try:
        if 'signout' == request.session['uid'] or not request.session['uid'] or not request.session['role']:
            return render(request, template_name='index.html')
        elif request.session['role'] == 'TEACHER':
            return render(request, template_name='usersappmainteacher.html')
        elif request.session['role'] == 'ADMIN':
            return render(request, template_name='dashboard.html')
    except Exception:
        return render(request, template_name='index.html')


def adminbaseaccount(request):
    try:
        if 'signout' == request.session['uid'] or not request.session['uid']:
            return render(request, template_name='index.html')
        elif request.session['role'] == 'ADMIN':
            data = requests.get('http://127.0.0.1:8000/app/appteacher/getall/', headers=headers)
            datastudent = requests.get('http://127.0.0.1:8000/app/appstudent/getall/', headers=headers)

            return render(request, template_name='users.html',
                          context={"datateacher": data.json(), "datastudent": datastudent.json()})
        else:
            return render(request, template_name='index.html')
    except Exception:
        return render(request, template_name='index.html')


def adminappsession(request):
    if 'POST' == request.method:
        request.session['uid'] = 'signout'
        del request.session['uid']
        return render(request, template_name='index.html')


# teacher

@ensure_csrf_cookie
def appteachergetall(request):
    try:
        if request.session['role'] == 'ADMIN':
            role = Role.objects.filter(name="TEACHER").first()._id
            acc = Account.objects.filter(role=role)
            return HttpResponse(content=json.dumps([res.getall() for res in acc]), content_type="application/json",
                                status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def appteachercreate(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            username = dict_keys.get('username')
            image = dict_keys.get('image')
            infofullname = dict_keys.get('fullname')
            infoemail = dict_keys.get('email')
            password = dict_keys.get('password')
            namefile = dict_keys.get('namefile')

            role = Role.objects.filter(name="TEACHER").first()._id
            info = InfoTeacher(fullname=infofullname, email=infoemail)

            formatd, imgstr = image.split(';base64,')
            ext = formatd.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=namefile)

            # save file image and get path

            link = "account/%02d/%02d/%02d" % (
                datetime.today().year, datetime.today().month, datetime.today().day)

            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, link)
                                   , base_url=os.path.join(settings.MEDIA_ROOT, link))
            filename = fs.save(data.name, data)
            # uploaded_file_url = fs.url(filename)

            accountteacher = Account(name=username, role_id=role, image=os.path.join(link, filename), password=password,
                                     info=info)
            accountteacher.save()

            return HttpResponse(content=json.dumps(accountteacher.getall()), content_type='application/json',
                                status=200)

    except Exception:
        pass


@ensure_csrf_cookie
def appteacherdelete(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            idrow = dict_keys.get('idrow')
            print(idrow)
            accdelete = Account(pk=idrow)
            accdelete.delete()
            return HttpResponse(content="", content_type='application/json',
                                status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def appteacherupdate(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            username = dict_keys.get('username')
            image = dict_keys.get('image')
            fullname = dict_keys.get('fullname')
            email = dict_keys.get('email')
            password = dict_keys.get('password')
            namefile = dict_keys.get('namefile')
            changepass = dict_keys.get('changepass')
            changeimage = dict_keys.get('changeimage')
            idrow = dict_keys.get('idrow')

            if changepass and not changeimage:
                acc = Account.objects.filter(pk=idrow).first()
                acc.name = username
                acc.info.fullname = fullname
                acc.info.email = email
                acc.password = pwd_context.hash(password)
                acc.saveupdate()

            if changeimage and not changepass:
                Account(pk=idrow).deleteimage()

                formatd, imgstr = image.split(';base64,')
                ext = formatd.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=namefile)

                link = "account/%02d/%02d/%02d" % (
                    datetime.today().year, datetime.today().month, datetime.today().day)

                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, link)
                                       , base_url=os.path.join(settings.MEDIA_ROOT, link))
                filename = fs.save(data.name, data)

                acc = Account.objects.filter(pk=idrow).first()
                acc.name = username
                acc.info.fullname = fullname
                acc.info.email = email
                acc.image = os.path.join(link, filename)
                acc.saveupdate()

            if changepass and changeimage:
                Account(pk=idrow).deleteimage()

                formatd, imgstr = image.split(';base64,')
                ext = formatd.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=namefile)

                link = "account/%02d/%02d/%02d" % (
                    datetime.today().year, datetime.today().month, datetime.today().day)

                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, link)
                                       , base_url=os.path.join(settings.MEDIA_ROOT, link))
                filename = fs.save(data.name, data)

                acc = Account.objects.filter(pk=idrow).first()
                acc.name = username
                acc.info.fullname = fullname
                acc.info.email = email
                acc.password = pwd_context.hash(password)
                acc.image = os.path.join(link, filename)
                acc.saveupdate()

            if not changepass and not changeimage:
                acc = Account.objects.filter(pk=idrow).first()
                acc.name = username
                acc.info.fullname = fullname
                acc.info.email = email
                acc.saveupdate()

            return HttpResponse(content="", content_type='application/json',
                                status=200)
    except Exception:
        pass


# end teacher

# student
@ensure_csrf_cookie
def appstudentgetall(request):
    try:
        if request.session['role'] == 'ADMIN':
            role = Role.objects.filter(name="STUDENT").first()._id
            acc = Account.objects.filter(role=role)
            return HttpResponse(content=json.dumps([res.getall() for res in acc]), content_type="application/json",
                                status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def appstudentcreate(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            username = dict_keys.get('username')
            image = dict_keys.get('image')
            infofullname = dict_keys.get('fullname')
            infoemail = dict_keys.get('email')
            password = dict_keys.get('password')
            namefile = dict_keys.get('namefile')

            role = Role.objects.filter(name="STUDENT").first()._id
            info = InfoTeacher(fullname=infofullname, email=infoemail)

            formatd, imgstr = image.split(';base64,')
            ext = formatd.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=namefile)

            # save file image and get path

            link = "account/%02d/%02d/%02d" % (
                datetime.today().year, datetime.today().month, datetime.today().day)

            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, link)
                                   , base_url=os.path.join(settings.MEDIA_ROOT, link))
            filename = fs.save(data.name, data)
            # uploaded_file_url = fs.url(filename)

            accountteacher = Account(name=username, role_id=role, image=os.path.join(link, filename), password=password,
                                     info=info)
            accountteacher.save()

            return HttpResponse(content=json.dumps(accountteacher.getall()), content_type='application/json',
                                status=200)

    except Exception:
        pass


@ensure_csrf_cookie
def appstudentdelete(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            idrow = dict_keys.get('idrow')
            print(idrow)
            accdelete = Account(pk=idrow)
            accdelete.delete()
            return HttpResponse(content="", content_type='application/json',
                                status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def appstudentupdate(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            username = dict_keys.get('username')
            image = dict_keys.get('image')
            fullname = dict_keys.get('fullname')
            email = dict_keys.get('email')
            password = dict_keys.get('password')
            namefile = dict_keys.get('namefile')
            changepass = dict_keys.get('changepass')
            changeimage = dict_keys.get('changeimage')
            idrow = dict_keys.get('idrow')

            if changepass and not changeimage:
                acc = Account.objects.filter(pk=idrow).first()
                acc.name = username
                acc.info.fullname = fullname
                acc.info.email = email
                acc.password = pwd_context.hash(password)
                acc.saveupdate()

            if changeimage and not changepass:
                Account(pk=idrow).deleteimage()

                formatd, imgstr = image.split(';base64,')
                ext = formatd.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=namefile)

                link = "account/%02d/%02d/%02d" % (
                    datetime.today().year, datetime.today().month, datetime.today().day)

                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, link)
                                       , base_url=os.path.join(settings.MEDIA_ROOT, link))
                filename = fs.save(data.name, data)

                acc = Account.objects.filter(pk=idrow).first()
                acc.name = username
                acc.info.fullname = fullname
                acc.info.email = email
                acc.image = os.path.join(link, filename)
                acc.saveupdate()

            if changepass and changeimage:
                Account(pk=idrow).deleteimage()

                formatd, imgstr = image.split(';base64,')
                ext = formatd.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=namefile)

                link = "account/%02d/%02d/%02d" % (
                    datetime.today().year, datetime.today().month, datetime.today().day)

                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, link)
                                       , base_url=os.path.join(settings.MEDIA_ROOT, link))
                filename = fs.save(data.name, data)

                acc = Account.objects.filter(pk=idrow).first()
                acc.name = username
                acc.info.fullname = fullname
                acc.info.email = email
                acc.password = pwd_context.hash(password)
                acc.image = os.path.join(link, filename)
                acc.saveupdate()

            if not changepass and not changeimage:
                acc = Account.objects.filter(pk=idrow).first()
                acc.name = username
                acc.info.fullname = fullname
                acc.info.email = email
                acc.saveupdate()

            return HttpResponse(content="", content_type='application/json',
                                status=200)
    except Exception:
        pass


# end student

@ensure_csrf_cookie
def appcategory(request):
    try:
        if 'signout' == request.session['uid'] or not request.session['uid']:
            return render(request, template_name='index.html')
        elif request.session['role'] == 'ADMIN':
            return render(request, template_name='category.html')
        else:
            return render(request, template_name='index.html')
    except Exception:
        return render(request, template_name='index.html')


@ensure_csrf_cookie
def appcategorycreate(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            namecourse = dict_keys.get('namecourse')
            subcourse = dict_keys.get('subcourse')

            categorycourse = CategoryCourse()
            children = []
            if subcourse:
                scate = dict()
                for res in subcourse:
                    sub = SubCateCourse(namesubcourse=res['namesubcourse'])
                    sub.save()
                    scate[str(sub.pk)] = res['namesubcourse']

                subcate = [SubCateCourse(namesubcourse=scate[key], subcoursecode=key) for key in
                           scate.keys()]
                categorycourse.subcourse = subcate
                children = scate
            else:
                categorycourse.subcourse = []

            categorycourse.namecourse = namecourse
            categorycourse.save()

            pkcategoryroot = categorycourse.pk

            if children:
                jsonchildren = []
                for key in children:
                    print(key, children[key])
                    jsonchildren.append({"name": children[key], "id": key})
                result = {
                    "name": namecourse,
                    "id": str(pkcategoryroot),
                    "children": jsonchildren
                }
                return HttpResponse(content=json.dumps(result), content_type='application/json',
                                    status=200)
            else:
                result = {
                    "name": namecourse,
                    "id": str(pkcategoryroot),
                    "children": []
                }
                return HttpResponse(content=json.dumps(result), content_type='application/json',
                                    status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def appcategorygetdata(request):
    try:
        if request.method == 'POST':
            dataresult = []
            for category in CategoryCourse.objects.all():
                if category.subcourse:
                    dataserialize = json.loads(serialize('json', category.subcourse))
                    children = []
                    for val in dataserialize:
                        fields = json.loads(json.dumps(val)).get('fields')
                        children.append({"name": fields.get('namesubcourse'), "id": fields.get('subcoursecode')})
                    dataresult.append(
                        {"name": category.namecourse, "id": str(category.pk),
                         "children": children})
                else:
                    dataresult.append(
                        {"name": category.namecourse, "id": str(category.pk),
                         "children": []})
            return HttpResponse(content=json.dumps(dataresult), content_type="application/json",
                                status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def appcategorydelete(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            pk = dict_keys.get('pk')
            categorycourse = CategoryCourse.objects.filter(pk=pk).first()
            categorycourse.delete()
            if categorycourse.subcourse:
                subcate = SubCateCourse()
                for val in [val.subcoursecode for val in categorycourse.subcourse]:
                    subcate.pk = val
                    subcate.delete()

            return HttpResponse(content="", content_type="application/json",
                                status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def appcategorygetnav(request):
    try:
        if request.method == 'POST':
            data = [val.getall() for val in CategoryCourse.objects.filter().all()]
            return HttpResponse(content=json.dumps(data), content_type="application/json",
                                status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def appcategoryrootname(request, rootname):
    try:
        if request.method == 'GET':
            if request.session['role'] == 'ADMIN':
                return render(request=request, template_name='course.html', context={"categorycourse": rootname})
            else:
                return render(request, template_name='index.html')
    except Exception:
        pass


@ensure_csrf_cookie
def appcategorysubname(request, subname):
    try:
        if request.method == 'GET':
            if request.session['role'] == 'ADMIN':
                return render(request=request, template_name='course.html', context={"categorycourse": subname})
            else:
                return render(request, template_name='index.html')
    except Exception:
        pass


# students
@ensure_csrf_cookie
def adminbasestudents(request):
    try:
        if 'signout' == request.session['uid'] or not request.session['uid']:
            return render(request, template_name='index.html')
        elif request.session['role'] == 'ADMIN':
            datastudentinfo = requests.get('http://localhost:8000/app/appstudentinfo/getall/', headers=headers)
            return render(request, template_name='students.html', context={"datastudentinfo": datastudentinfo.json()})
        else:
            return render(request, template_name='index.html')
    except Exception:
        return render(request, template_name='index.html')


@ensure_csrf_cookie
def adminstudentsgetall(request):
    try:
        if request.session['role'] == 'ADMIN':
            student = Student.objects.filter().all()
            return HttpResponse(content=json.dumps([res.getall() for res in student]), content_type="application/json",
                                status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def adminstudentscreate(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            fullname = dict_keys.get('fullname')
            hometown = dict_keys.get('hometown')
            birthday = dict_keys.get('birthday')
            school = dict_keys.get('school')
            graduationtime = dict_keys.get('graduationtime')
            face = dict_keys.get('face')
            email = dict_keys.get('email')
            phone = dict_keys.get('phone')
            # coursecode = dict_keys.get('coursecode')
            # studentcode = dict_keys.get('studentcode')
            accountcode = dict_keys.get('accountcode')
            namefile = dict_keys.get('namefile')

            formatd, imgstr = face.split(';base64,')
            ext = formatd.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=namefile)

            # save file image and get path

            link = "student/%02d/%02d/%02d" % (
                datetime.today().year, datetime.today().month, datetime.today().day)

            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, link)
                                   , base_url=os.path.join(settings.MEDIA_ROOT, link))
            filename = fs.save(data.name, data)

            resbirthday = datetime.strptime(birthday, "%Y-%m-%dT%H:%M:%S.%fZ")
            strbirthday = '%02d-%02d-%02d' % (resbirthday.year, resbirthday.month, resbirthday.day)

            resgraduationtime = datetime.strptime(graduationtime, "%Y-%m-%dT%H:%M:%S.%fZ")
            strgraduationtime = '%02d-%02d-%02d' % (
                resgraduationtime.year, resgraduationtime.month, resgraduationtime.day)

            students = Student(fullname=fullname, hometown=hometown, birthday=strbirthday, school=school,
                               graduationtime=strgraduationtime, face=os.path.join(link, filename), email=email,
                               phone=phone, accountcode=accountcode)
            students.save()

            resstudents = students.getall()

            return HttpResponse(content=json.dumps(resstudents), content_type='application/json',
                                status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def adminstudentsupdate(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))

            fullname = dict_keys.get('fullname')
            hometown = dict_keys.get('hometown')
            birthday = dict_keys.get('birthday')
            school = dict_keys.get('school')
            graduationtime = dict_keys.get('graduationtime')
            face = dict_keys.get('face')
            email = dict_keys.get('email')
            phone = dict_keys.get('phone')
            # coursecode = dict_keys.get('coursecode')
            # studentcode = dict_keys.get('studentcode')
            accountcode = dict_keys.get('accountcode')
            changebirthday = dict_keys.get('changebirthday')
            changegraduationtime = dict_keys.get('changegraduationtime')

            namefile = dict_keys.get('namefile')
            changeimage = dict_keys.get('changeimage')
            idrow = dict_keys.get('idrow')

            if changeimage:
                Student(pk=idrow).deleteimage()

                formatd, imgstr = face.split(';base64,')
                ext = formatd.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=namefile)

                link = "student/%02d/%02d/%02d" % (
                    datetime.today().year, datetime.today().month, datetime.today().day)

                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, link)
                                       , base_url=os.path.join(settings.MEDIA_ROOT, link))
                filename = fs.save(data.name, data)

                if changebirthday and changegraduationtime:

                    resbirthday = datetime.strptime(birthday, "%Y-%m-%dT%H:%M:%S.%fZ")
                    strbirthday = '%02d-%02d-%02d' % (resbirthday.year, resbirthday.month, resbirthday.day)

                    resgraduationtime = datetime.strptime(graduationtime, "%Y-%m-%dT%H:%M:%S.%fZ")
                    strgraduationtime = '%02d-%02d-%02d' % (
                        resgraduationtime.year, resgraduationtime.month, resgraduationtime.day)

                    student = Student.objects.filter(pk=idrow).first()
                    student.fullname = fullname
                    student.hometown = hometown
                    student.birthday = strbirthday
                    student.school = school
                    student.graduationtime = strgraduationtime
                    student.face = os.path.join(link, filename)
                    student.email = email
                    student.phone = phone
                    student.accountcode = accountcode
                    student.saveupdate()
                elif changebirthday:
                    resbirthday = datetime.strptime(birthday, "%Y-%m-%dT%H:%M:%S.%fZ")
                    strbirthday = '%02d-%02d-%02d' % (resbirthday.year, resbirthday.month, resbirthday.day)

                    student = Student.objects.filter(pk=idrow).first()
                    student.fullname = fullname
                    student.hometown = hometown
                    student.birthday = strbirthday
                    student.school = school
                    student.face = os.path.join(link, filename)
                    student.email = email
                    student.phone = phone
                    student.accountcode = accountcode
                    student.saveupdate()
                elif changegraduationtime:
                    resgraduationtime = datetime.strptime(graduationtime, "%Y-%m-%dT%H:%M:%S.%fZ")
                    strgraduationtime = '%02d-%02d-%02d' % (
                        resgraduationtime.year, resgraduationtime.month, resgraduationtime.day)

                    student = Student.objects.filter(pk=idrow).first()
                    student.fullname = fullname
                    student.hometown = hometown
                    student.school = school
                    student.graduationtime = strgraduationtime
                    student.face = os.path.join(link, filename)
                    student.email = email
                    student.phone = phone
                    student.accountcode = accountcode
                    student.saveupdate()
                elif not changebirthday and not changegraduationtime:
                    student = Student.objects.filter(pk=idrow).first()
                    student.fullname = fullname
                    student.hometown = hometown
                    student.school = school
                    student.face = os.path.join(link, filename)
                    student.email = email
                    student.phone = phone
                    student.accountcode = accountcode
                    student.saveupdate()

            if not changeimage:
                if changebirthday and changegraduationtime:
                    resbirthday = datetime.strptime(birthday, "%Y-%m-%dT%H:%M:%S.%fZ")
                    strbirthday = '%02d-%02d-%02d' % (resbirthday.year, resbirthday.month, resbirthday.day)

                    resgraduationtime = datetime.strptime(graduationtime, "%Y-%m-%dT%H:%M:%S.%fZ")
                    strgraduationtime = '%02d-%02d-%02d' % (
                        resgraduationtime.year, resgraduationtime.month, resgraduationtime.day)

                    student = Student.objects.filter(pk=idrow).first()
                    student.fullname = fullname
                    student.hometown = hometown
                    student.birthday = strbirthday
                    student.school = school
                    student.graduationtime = strgraduationtime
                    student.email = email
                    student.phone = phone
                    student.accountcode = accountcode
                    student.save()
                elif changebirthday:
                    resbirthday = datetime.strptime(birthday, "%Y-%m-%dT%H:%M:%S.%fZ")
                    strbirthday = '%02d-%02d-%02d' % (resbirthday.year, resbirthday.month, resbirthday.day)

                    student = Student.objects.filter(pk=idrow).first()
                    student.fullname = fullname
                    student.hometown = hometown
                    student.birthday = strbirthday
                    student.school = school
                    student.email = email
                    student.phone = phone
                    student.accountcode = accountcode
                    student.save()
                elif changegraduationtime:
                    resgraduationtime = datetime.strptime(graduationtime, "%Y-%m-%dT%H:%M:%S.%fZ")
                    strgraduationtime = '%02d-%02d-%02d' % (
                        resgraduationtime.year, resgraduationtime.month, resgraduationtime.day)

                    student = Student.objects.filter(pk=idrow).first()
                    student.fullname = fullname
                    student.hometown = hometown
                    student.school = school
                    student.graduationtime = strgraduationtime
                    student.email = email
                    student.phone = phone
                    student.accountcode = accountcode
                    student.save()
                elif not changebirthday and not changegraduationtime:
                    student = Student.objects.filter(pk=idrow).first()
                    student.fullname = fullname
                    student.hometown = hometown
                    student.school = school
                    student.email = email
                    student.phone = phone
                    student.accountcode = accountcode
                    student.save()

            return HttpResponse(content="", content_type='application/json',
                                status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def adminstudentsdelete(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            pk = dict_keys.get('idrow')
            student = Student(pk=pk)
            student.delete()
            return HttpResponse(content="", content_type="application/json",
                                status=200)
    except Exception:
        pass


# endstudents

# course
@ensure_csrf_cookie
def createcourse(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            namecourse = dict_keys.get('name')
            coursecode = dict_keys.get('coursecode')
            startdate = dict_keys.get('startdate')
            enddate = dict_keys.get('enddate')
            imagecourse = dict_keys.get('image')
            namefile = dict_keys.get('namefile')
            teacher = dict_keys.get('teachervalue')
            categorycourse = dict_keys.get('catecourse')
            tname = teacher['name']
            tidteacher = teacher['idteacher']

            formatd, imgstr = imagecourse.split(';base64,')
            ext = formatd.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=namefile)

            # save file image and get path

            link = "course/%02d/%02d/%02d" % (
                datetime.today().year, datetime.today().month, datetime.today().day)

            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, link)
                                   , base_url=os.path.join(settings.MEDIA_ROOT, link))
            filename = fs.save(data.name, data)

            resstartdate = datetime.strptime(startdate, "%Y-%m-%dT%H:%M:%S.%fZ")
            strstartdate = '%02d-%02d-%02d' % (resstartdate.year, resstartdate.month, resstartdate.day)

            resenddate = datetime.strptime(enddate, "%Y-%m-%dT%H:%M:%S.%fZ")
            strenddate = '%02d-%02d-%02d' % (resenddate.year, resenddate.month, resenddate.day)

            obteacher = Teacher(fullname=tname, account=tidteacher)
            course = Course(namecourse=namecourse, startdate=strstartdate, enddate=strenddate,
                            imagecourse=os.path.join(link, filename),
                            teacher=obteacher, coursecode=coursecode, categorycourse=categorycourse)

            course.save()

            rescourse = course.getallc()

            return HttpResponse(content=json.dumps(rescourse), content_type="application/json", status=200)
    except Exception:
        return HttpResponse(content="", content_type="application/json", status=200)


@ensure_csrf_cookie
def updatecourse(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            data = dict_keys.get('data')
            categorycourse = dict_keys.get('categorycourse')
            infoc = dict_keys.get('infoc')

            course = Course.objects.filter(pk=infoc, categorycourse=categorycourse).first()
            liststudentid = []
            for val in json.loads(data):
                v = dict(val)
                liststudentid.append(v['id'])
            course.student_id = liststudentid
            course.save()
            return HttpResponse(content=categorycourse, content_type="application/json",
                                status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def deletecourse(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            categorycourse = dict_keys.get('categorycourse')
            infoc = dict_keys.get('infoc')
            course = Course.objects.filter(pk=infoc, categorycourse=categorycourse).first()
            course.delete()
            return HttpResponse(content=categorycourse, content_type="application/json",
                                status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def coursegetallsearch(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            namecourse = dict_keys.get('catecourse')
            perpage = dict_keys.get('perpage')
            currentPage = dict_keys.get('currentPage')

            # search
            namesearch = dict_keys.get('namesearch')
            startdate = dict_keys.get('startdate')
            enddate = dict_keys.get('enddate')
            # end search

            if not startdate and not enddate:
                offset = (currentPage - 1) * perpage
                if Course.objects.filter(categorycourse__contains=namecourse).count() == 0:
                    result = json.dumps({"total": 0, "data": []})
                    return HttpResponse(content=result, content_type="application/json", status=200)
                elif Course.objects.filter(categorycourse__contains=namecourse).count() > 0 \
                        and str(namesearch).__len__() > 0:

                    totaldata = Course.objects.filter(categorycourse__contains=namecourse,
                                                      namecourse__contains=namesearch).count()
                    rescourse = Course.objects.filter(categorycourse__contains=namecourse,
                                                      namecourse__contains=namesearch)[offset:offset + perpage]
                    datalist = [val.getall() for val in rescourse]
                    result = json.dumps({"total": totaldata, "data": datalist})
                    return HttpResponse(content=result, content_type="application/json", status=200)
                elif Course.objects.filter(categorycourse__contains=namecourse).count() > 0 \
                        and str(namesearch).__len__() == 0:
                    totaldata = Course.objects.filter(categorycourse__contains=namecourse).count()
                    rescourse = Course.objects.filter(categorycourse__contains=namecourse)[offset:offset + perpage]
                    datalist = [val.getall() for val in rescourse]
                    result = json.dumps({"total": totaldata, "data": datalist})
                    return HttpResponse(content=result, content_type="application/json", status=200)

            if startdate and enddate:
                offset = (currentPage - 1) * perpage
                totaldata = Course.objects.filter(categorycourse__contains=namecourse,
                                                  namecourse__contains=namesearch,
                                                  startdate__gte=startdate,
                                                  enddate__lte=enddate).count()
                rescourse = Course.objects.filter(categorycourse__contains=namecourse,
                                                  namecourse__contains=namesearch,
                                                  startdate__gte=startdate,
                                                  enddate__lte=enddate)[offset:offset + perpage]
                datalist = [val.getall() for val in rescourse]
                result = json.dumps({"total": totaldata, "data": datalist})
                return HttpResponse(content=result, content_type="application/json", status=200)
    except Exception:
        pass


@ensure_csrf_cookie
def coursegetinfosub(request, subname, info):
    try:
        if request.method == 'GET':
            if request.session['role'] == 'ADMIN':
                course = Course.objects.filter(pk=info).first()
                datastudentinfo = requests.get('http://localhost:8000/app/appstudentinfo/getall/', headers=headers)
                return render(request=request, template_name='coursedetail.html',
                              context={"categorycourse": subname, "infoc": info, "datacourse": course.getall(),
                                       "datastudentinfo": datastudentinfo.json(), "location": "sub"})
            else:
                return render(request, template_name='index.html')
    except Exception:
        pass


@ensure_csrf_cookie
def coursegetinforoot(request, rootname, info):
    try:
        if request.method == 'GET':
            if request.session['role'] == 'ADMIN':
                course = Course.objects.filter(pk=info).first()
                datastudentinfo = requests.get('http://localhost:8000/app/appstudentinfo/getall/', headers=headers)
                return render(request=request, template_name='coursedetail.html',
                              context={"categorycourse": rootname, "infoc": info, "datacourse": course.getall(),
                                       "datastudentinfo": datastudentinfo.json(), "location": "root"})
            else:
                return render(request, template_name='index.html')
    except Exception:
        pass


@ensure_csrf_cookie
def coursegetstudentin(request):
    try:
        if request.method == 'POST':
            dict_keys = dict(json.loads(request.body))
            categorycourse = dict_keys.get('categorycourse')
            infoc = dict_keys.get('infoc')
            print(categorycourse, infoc)

            course = Course.objects.filter(pk=infoc).first()
            liststudent = []
            for val in course.student_id:
                student = Student.objects.filter(pk=val).first()
                liststudent.append(student.getall())

            return HttpResponse(content=json.dumps(liststudent), content_type="application/json",
                                status=200)
    except Exception:
        pass
# end course
