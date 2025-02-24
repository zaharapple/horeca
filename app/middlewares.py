from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token


class InitialSessionKeyMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if not request.session.session_key:
            request.session.create()
        get_token(request)
