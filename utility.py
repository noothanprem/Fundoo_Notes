import json

import jwt
# import settings
from django.conf import settings
from django.contrib.auth.models import User
from django_short_url.models import ShortURL
from django_short_url.views import get_surl

response = {"success": False,
            "message": "",
            "data": []}


def smd_response(self, success, message, data):
    self.response['success'] = success
    self.response['message'] = message
    self.response['data'] = data
    return self.response



class Response:

    def smd_response(self,success,message,data):
        response = {"success": False,
                    "message": "",
                    "data": []}

        response['success'] = success
        response['message'] = message
        response['data'].append(data)
        return response

    def json_response(self,response_data):

        data_in_json = json.dumps(response_data)
        return data_in_json


class Crypto:
    algo = 'HS256'
    __secret = settings.SECRET_KEY

    #def __init__(self, *args, **kwargs):

        # self.algo =
        # pass

    def encode_token(self, payload):
        jwt_token = {"token": jwt.encode(payload, self.__secret, algorithm="HS256").decode('utf-8')}
        token = jwt_token['token']
        return token

    def decode_token(self, token):
        tokenobj = ShortURL.objects.get(surl=token)
        tokens = tokenobj.lurl
        print(tokens)
        user_details = jwt.decode(tokens, self.__secret, algorithms='HS256')
        username = user_details['username']
        return username

    def short_url(self, key):
        url = str(key)
        surl = get_surl(url)
        short = surl.split("/")
        return short
