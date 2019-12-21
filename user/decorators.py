import redis
from django.http import HttpResponse
from .lib.redis_function import RedisOperation
redisobject = RedisOperation()
redisobject.__connect__()



# decorator to check whether the token is valid or not
def token_required(view_func):
    def wrap(r, request, *args, **kwargs):

        # getting the request header
        try:
            header = request.META['HTTP_AUTHORIZATION']
        except Exception:
            print ("Exception occured while accessing the request header")

        # splitting the header to make a list
        headerlist = header.split(" ")

        # getting the token from the list

        headertoken = headerlist[1]

        # trying to access the token from redis using the token got from request header
        redistoken = redisobject.get(headertoken)

        # If we got the token in redis, then the token is valid. so, move forward
        if redistoken is not None:
            return view_func(r, request, *args, **kwargs)
        else:
            return HttpResponse("Logout unsuccessful")

    return wrap
