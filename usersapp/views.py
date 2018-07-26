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
from adminapp.models import SubCateCourse, CategoryCourse, Course


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
