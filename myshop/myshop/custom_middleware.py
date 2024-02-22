from django.urls import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME

class Auth2RequiredException(Exception):
    pass


class Custom2fAMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.headers._store['auth2fa-code'] = ('AUTH2FA_CODE', 1234)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        print('after')

        return response


