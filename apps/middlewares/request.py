import threading
from django.utils.deprecation import MiddlewareMixin


class AppRequestMiddleware(MiddlewareMixin):
    _request = {}

    def process_request(self, request):
        self.__class__.set_request(request)

    def process_response(self, request, response):
        self.__class__.del_request()
        return response

    def process_exception(self, request, exception):
        self.__class__.del_request()

    @classmethod
    def get_request(cls, default=None):
        return cls._request.get(threading.current_thread(), default)

    @classmethod
    def set_request(cls, request):
        cls._request[threading.current_thread()] = request

    @classmethod
    def del_request(cls):
        cls._request.pop(threading.current_thread(), None)
