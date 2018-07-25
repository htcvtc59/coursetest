from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from assets.validtoken import *
import json


# Create your views here.


def index(request):
    request.session['token'] = createtoken(USERNAME,PASSWORD)
    return render(request, 'index.html')
