from __future__ import unicode_literals

import pdb

from django.core.validators import validate_email
from user.serializers import UserSerializer, LoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, \
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
from django_short_url.views import get_surl
# import templates
from django_short_url.models import ShortURL
import os
from user.lib.redis_function import RedisOperation
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
import os
from .jwt import GenerateToken
from jwt.exceptions import DecodeError
from redis.exceptions import ConnectionError, AuthenticationError
from user.lib.event_emitter import ee
from validate_email import validate_email
from utility import Crypto,Response
from decouple import config

response_class_object = Response()
token_generation_object = GenerateToken()
redis_object = RedisOperation()
redis_object.__connect__()

jwt_class_object = Crypto()
class UserOperations:


    def register_user(self, request):
        """
        :param request: to register the user
        :return: registers the user
        """

        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']


            is_valid=validate_email(email)
            if is_valid == False:
                response=self.smd_response(False, 'Email is Invalid','')
            else:


                if ((User.objects.filter(username=username).exists()) or (User.objects.filter(email=email).exists())):

                    response = response_class_object.smd_response(False, 'Username or email alredy exists', '')
                    return response

                elif username == "" or password == '' or email == '':

                    response = response_class_object.smd_response(False, 'Username or email is empty', '')
                    return response
                else:

                    user = User.objects.create_user(username=username, email=email, password=password)

                    user.is_active = False
                    user.save()

                    payload = {
                        'username': user.username,
                        'email': user.email
                    }

                    token = jwt_class_object.encode_token(payload)

                    currentsite = get_current_site(request)

                    splittedshortedtokenstr = jwt_class_object.short_url(token)

                    mail_subject = 'Link to activate the account'
                    mail_message = render_to_string('activate.html', {
                        'user': user.username,
                        'domain': get_current_site(request).domain,
                        'token': splittedshortedtokenstr[2],
                    })

                    recipient_email = config('EMAILID')

                    ee.emit('send_mail',recipient_email,mail_message)
                    #email = EmailMessage(mail_subject, mail_message, to=[recipient_email])

                    #email.send()
                    response = response_class_object.smd_response(True, 'Please check your mail for activating', '')
                    return response
        except SMTPException:
            response = response_class_object.smd_response(False, 'Exception while sending mail', '')
        except User.DoesNotExist:
            response = response_class_object.smd_response(False, 'Exception while getting the user using filter', '')
        except DecodeError:
            response = response_class_object.smd_response(False, 'Exception while generating the token', '')

        return response

    def login_user(self, request):
        """
        :param request: request to login user
        :return: logins the user
        """

        try:

            #pdb.set_trace()
            username = request.data['username']
            password = request.data['password']

            if username == "" or password == '':
                response = response_class_object.smd_response(False, 'Username or Password is empty', '')
                return response

            user = auth.authenticate(username=username, password=password)


            if user is not None:

                auth.login(request, user)

                payload = {
                    'username': username,
                    'password': password
                }


                token=token_generation_object.login_token(payload)


                user=request.user
                user_id=user.id
                #redis_object.set("loginuser",user_id)
                redis_object.set(token,user_id)

                response = response_class_object.smd_response(True, 'Login Success', token)

                return response
            else:

                response = response_class_object.smd_response(False, 'Login Failed', '')

                return response
        except DecodeError:
            response = response_class_object.smd_response(False, 'Exception while generating token', '')

        except PermissionDenied:
            response = response_class_object.smd_response(False, 'Exception while authenticating user', '')

        except ConnectionError:
            response = response_class_object.smd_response(False, 'Exception in redis operation-ConnectionError', '')

        except AuthenticationError:
            response = response_class_object.smd_response(False, 'Exception in redis operation-AuthenticationError', '')


        return response


    def forgot_password(self, request):
        """
        :param request: for forgot password
        :return: send the mail with token
        """

        try:

            emailid = request.data['email']

            if emailid == '':
                response = response_class_object.smd_response(False, 'email is empty', '')
                return response

            user = User.objects.get(email=emailid)

            if user is not None:

                payload = {
                    'username': user.username,
                    'email': user.email
                }

                jwt_token = {"token": jwt.encode(payload, "secret", algorithm="HS256").decode('utf-8')}

                token = jwt_token["token"]
                currentsite = get_current_site(request)
                subject = "Link to Reset the password"

                message = render_to_string('forgotpassword.html', {
                    'domain': get_current_site(request).domain,
                    'token': token
                })
                sender = os.getenv('EMAIL_HOST_USER')
                reciever = os.getenv('EMAILID')


                send_mail(subject, message, sender, [reciever])

                response = response_class_object.smd_response(True, 'Check your mail for the link', '')
                return response

            else:

                response = response_class_object.smd_response(False, 'Invalid Email id.. Try Once again', '')
                return response
        except SMTPException:
            response = response_class_object.smd_response(False, 'Exception occured while sending email', '')
        except DecodeError:
            response = response_class_object.smd_response(False, 'Exception occured while generating token', '')
        except User.DoesNotExist:
            response = response_class_object.smd_response(False, 'Exception occured while getting the user object', '')
        return response

    def reset_password(self, request, token):
        """
        :param request: for resetting the password
        :param token: token obtained from the url
        :return: resets the password
        """

        try:

            user_details = jwt.decode(token, "secret")
            user_name = user_details['username']
            userobject = User.objects.get(username=user_name)

            if userobject is not None:
                password = request.data['password']
            else:
                response = response_class_object.smd_response(False, 'Invalid User', '')
                return response

            user = User.objects.get(username=user_name)
            if user is not None:
                user.set_password(password)

                user.save()
                response = response_class_object.smd_response(True, 'Passsword Changed Successfully', '')

                return response

            else:

                response = response_class_object.smd_response(False, 'Both the Passwords doesnt match', '')

                return response
        except User.DoesNotExist:
            response = response_class_object.smd_response(False, 'Exception occured while accessing the user object', [])
        except DecodeError:
            response = response_class_object.smd_response(False, 'Exception occured while generating the token', [])
        return response

    def logout(self, request):

        try:
            header = request.META['HTTP_AUTHORIZATION']

            headerlist = header.split(" ")
            token = headerlist[1]

            redis_object.delete(token)

            response = response_class_object.smd_response(True, 'Logout Successful', [])
            return response
        except ConnectionError:
            response = response_class_object.smd_response(False, 'Exception occured while accessing redis-ConnectionError', [])
        except AuthenticationError:
            response = response_class_object.smd_response(False, 'Exception occured while accessing redis-AuthenticationError', [])
        return response

    def activate(self, request, token):
        """
        :param request: to activate the user
        :param token: takes the token from the url
        :return: activates the user
        """

        try:

            user_name = jwt_class_object.decode_token(token)
            user = User.objects.get(username=user_name)

            if user is not None:
                user.is_active = True
                user.save()
                response = response_class_object.smd_response(True, 'Registration Successful', [])
                return response

            else:
                response = response_class_object.smd_response(False, 'Registration Failed', [])

                return response
        except User.DoesNotExist:
            response = response_class_object.smd_response(False, 'Exception occurred while getting the user object', [])
        except DecodeError:
            response = response_class_object.smd_response(False, 'Exception occurred while decoding the token', [])
        return response
