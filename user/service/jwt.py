import requests
import json

from django.http.response import HttpResponse


class GenerateToken:

    def login_token(self, payload):

        # try:
        AUTH_ENDPOINT = "http://127.0.0.1:8000/api/token/"
        print(payload)
        #response = requests.post(AUTH_ENDPOINT, data=data)
        token=requests.post(AUTH_ENDPOINT, data=payload)
        print (token)
        response=token.json()['access']
        return response
        # except Exception:
        # return False
