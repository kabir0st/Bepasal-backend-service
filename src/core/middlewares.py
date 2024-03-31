import logging

from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler
from rest_framework.pagination import PageNumberPagination
from django.conf import settings


def get_user(token):
    if user := cache.get(f'user_{cache.get(token)}'):
        return user
    else:
        return AnonymousUser


class APIAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if key := request.headers.get("authorization", None):
            request.user = get_user(key)
        return self.get_response(request)


class DisableCSRF(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, "_dont_enforce_csrf_checks", True)
        return self.get_response(request)


def core_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, Exception):
        error = str(exc)
        if hasattr(exc, 'detail'):
            error = exc.detail
        if isinstance(exc, ValidationError):
            error = ' / '.join([
                f"{key.capitalize()}: {e.capitalize()}" for key in exc.detail
                for e in exc.detail[key]
            ])
        err_data = {'status': False, 'error': error}
        logging.error(f"Original error detail and call stack: {exc}",
                      exc_info=settings.DEBUG)
        return JsonResponse(err_data, safe=False, status=503)
    return response


class PaginationMiddleware(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 100
