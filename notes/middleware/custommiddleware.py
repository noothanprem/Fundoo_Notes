import pdb

from rest_framework import status
from rest_framework_jwt.settings import api_settings

from notes.models import Note
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
from django.conf import settings
import jwt


class MyMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    # def __call__(self, request):
    #     print("Inside the middleware Before............")
    #
    #     response = {
    #         "success": False,
    #         "message": "Invalid User",
    #         "data": ""
    #     }
    #     # pdb.set_trace()
    #
    #     """
    #     getting the token from header if cookie method fails
    #     """
    #     print(request.META)
    #     http_header = request.META["HTTP_AUTHORIZATION"]
    #     token = http_header.split(" ")
    #     try:
    #         decoded_token = jwt.decode(token[1], settings.SECRET_KEY)
    #     except jwt.ExpiredSignatureError:
    #         print("Signature expired")
    #     user = User.objects.get(id=decoded_token['user_id'])
    #
    #     if user is None:
    #         return HttpResponse(json.dumps(response))
    #
    #     response = self.get_response(request)
    #     print("Inside the middleware After............")
    #     return response

    def __call__(self, request):
        url = request.path
        current_url = url.split("/")[1]
        if current_url == "127.0.0.1/api":
            try:
                print(request.META)
                token = request.META['HTTP_AUTHORIZATION']
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                new_token = str(token).split("Bearer ")[1]
                encoded_token = jwt_decode_handler(new_token)
                username = encoded_token['username']
                user = User.objects.get(username=username)
                try:
                    if user and user.is_active:
                        pass
                except User.DoesNotExist:
                    response_smd = {'status': False, 'message': 'Authentication Required'}
                    return HttpResponse(json.dumps(response_smd), status=status.HTTP_400_BAD_REQUEST)
            except KeyError:
                if request.session:
                    #pdb.set_trace()
                    user = request.user
                    if user.is_authenticated:
                        pass
                    else:
                        response_smd = {'status': False, 'message': 'Users credential not provided..!!'}
                        return HttpResponse(json.dumps(response_smd), status=status.HTTP_400_BAD_REQUEST)
                else:
                    response_smd = {'status': False, 'message': 'Users credential not provided..!!'}
                    return HttpResponse(json.dumps(response_smd), status=status.HTTP_400_BAD_REQUEST)
        else:
            return self.get_response(request)
