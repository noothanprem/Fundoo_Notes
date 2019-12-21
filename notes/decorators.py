import json
import pdb

import jwt
from django.conf import settings
from django.contrib.auth.models import User

from django.http import HttpResponse

from .lib.redis_function import RedisOperation

redisobject=RedisOperation()



def login_decorator(function):
    """

    :param function: Function which has to be wrapped
    :return: takes to the function if the user is valid
    """
    def wrapper(request, *args, **kwargs):
        response = {
            "success": False,
            "message": "Invalid User",
            "data": ""
        }

        """
        getting the token from header if cookie method fails
        """

        http_header = request.META["HTTP_AUTHORIZATION"]
        token = http_header.split(" ")
        try:
            decoded_token = jwt.decode(token[1], settings.SECRET_KEY)
        except jwt.ExpiredSignatureError:
            print ("Signature expired")
        user = User.objects.get(id=decoded_token['user_id'])

        if user is not None:
            return function(request, *args, **kwargs)
        else:
            return HttpResponse(json.dumps(response))
    return wrapper
