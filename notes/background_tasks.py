from __future__ import unicode_literals
from fundoo.setting.development import REMINDER_URL
import pdb

import requests
from django.shortcuts import render,HttpResponse
from background_task import background
# Create your views here.
@background(schedule=5)
def hello():

	requests.get(REMINDER_URL)

# def background_view(request):
# 	hello()
# 	return HttpResponse("Hello world !")