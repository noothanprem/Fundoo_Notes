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

    def __call__(self, request):
        response = {
            "success": False,
            "message": "Invalid User",
            "data": ""
        }

        """
        getting the token from header if cookie method fails
        """
        try:
            if request.META['HTTP_AUTHORIZATION']:
                http_header = request.META["HTTP_AUTHORIZATION"]
                token = http_header.split(" ")
                try:
                    decoded_token = jwt.decode(token[1], settings.SECRET_KEY)
                except jwt.ExpiredSignatureError:
                    print("Signature expired")
                user = User.objects.get(id=decoded_token['user_id'])

                if user is None:
                    return HttpResponse(json.dumps(response))
        except KeyError:
            pass
        response = self.get_response(request)
        return response


