from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
from .serializers import UserSerializer, LoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, \
    LogoutSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
import jwt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from smtplib import SMTPException
from django.utils.safestring import mark_safe
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
# import templates
from django_short_url.views import get_surl
from django_short_url.models import ShortURL
from .decorators import token_required
import redis
from .lib.redis_function import RedisOperation
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponseRedirect
from user.service import user
from utility import Response

userclassobject = user.UserOperations()
response_class_object = Response()


# API for registering the user
class Register(GenericAPIView):

    serializer_class = UserSerializer # setting the serializer class

    def post(self, request):

        response = userclassobject.register_user(request) # calling the register_user method in user.py
        final_response = response_class_object.json_response(response)
        if response['success'] == False:
            return HttpResponse(final_response,status=400)
        else:

            return HttpResponse(final_response,status=200) # string_user_registration=str(user_registration)


# API for login
class Login(GenericAPIView):

    serializer_class = LoginSerializer # setting the serializer class

    def post(self, request):
        request_data = request.data
        user = request.user
        response = userclassobject.login_user(request)
        final_response = response_class_object.json_response(response)
        if response['success'] == False:
            return HttpResponse(final_response,status=400)
        else:
            return HttpResponse(final_response,status=200)


# API for Forgot Password
class ForgotPassword(GenericAPIView):

    serializer_class = ForgotPasswordSerializer # Setting the serializer class

    def post(self, request):
        response = userclassobject.forgot_password(request)
        final_response  = response_class_object.json_response(response)
        if response['success'] == False:
            return HttpResponse(final_response,status=400)
        else:
            return HttpResponse(final_response,status=200)


# API for Reset password
class ResetPassword(GenericAPIView):
    serializer_class = ResetPasswordSerializer # setting the serializer class

    def post(self, request, **kwargs):
        # getting the token
        token = kwargs['token']
        response = userclassobject.reset_password(request, token)  # calling the reset_password method inside service
        final_response = response_class_object.json_response(response)
        if response['success'] == False:
            return HttpResponse(final_response,status=400)
        else:
            return HttpResponse(final_response,status=200)


# API for logout
class Logout(GenericAPIView):

    serializer_class = LogoutSerializer # setting the serializer class

    # using 'token_required' decorator
    @token_required
    def post(self, request):

        response = userclassobject.logout(request) # calling the logout method inside service
        final_response = response_class_object.json_response(response)
        return HttpResponse(final_response)


# method for activating the user
def activate(request, token):
    # calling the activate method inside service
    response = userclassobject.activate(request, token)
    final_response = response_class_object.json_response(response)
    return HttpResponse(final_response)


def sociallogin(request):
    return render(request, 'social_login.html')


def home(request):
    return render(request, 'home.html')



def get_user(id_):
    try:
        return User.objects.get(pk=id_)  # <-- tried to get by email here
    except User.DoesNotExist:
        return None


