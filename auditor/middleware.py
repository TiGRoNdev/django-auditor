"""
This module contains middleware which is needed to set current user to local thread

.. moduleauthor:: Igor Nazarov <tigron.dev@gmail.com>

"""
from .utils import _do_set_current_user


class AuditMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # request.user closure; asserts laziness;
        # memorization is implemented in
        # request.user (non-data descriptor)
        _do_set_current_user(lambda self: getattr(request, 'user', None))

        response = self.get_response(request)

        # Do something after

        return response
