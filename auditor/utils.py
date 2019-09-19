"""
This module provides useful uncategorized utilities for some processes in django-auditor

.. moduleauthor:: Igor Nazarov <tigron.dev@gmail.com>

"""
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from threading import local


USER_ATTR_NAME = getattr(settings, 'LOCAL_USER_ATTR_NAME', '_current_user')

_thread_locals = local()


def _do_set_current_user(user_fun):
    setattr(_thread_locals, USER_ATTR_NAME, user_fun.__get__(user_fun, local))


def _set_current_user(user=None):
    """
    Sets current user in local thread.
    """
    _do_set_current_user(lambda self: user)


def get_current_user():
    """
    Return current user if exists.
    """
    current_user = getattr(_thread_locals, USER_ATTR_NAME, None)
    if callable(current_user):
        return current_user()
    return current_user


def get_current_authenticated_user():
    """
    Return current user if authenticated.
    """
    current_user = get_current_user()
    if isinstance(current_user, AnonymousUser):
        return None
    return current_user


def is_equivalent(prev_instance, new_instance, fields=[]):
    """
    Return True if previous instance of object and new instance are equivalents
    """
    if fields:
        return all(
            [
                prev_instance.__dict__[key] == value
                for key, value in new_instance.__dict__.items()
                if key in fields
            ]
        )
    else:
        return all(
            [
                prev_instance.__dict__[key] == value
                for key, value in new_instance.__dict__.items()
                if not key.startswith('_')
            ]
        )


def auditor_to_raw_json(instance, fields):
    """
    Serialize Python-Django-model instance to raw JSON-string

    :param instance: Django-model instance
    :param fields: List of fields to serialize
    :return: raw JSON-string
    """
    if not fields:
        return str({name: value for name, value in instance.__dict__.items() if not str(name).startswith('_')})
    else:
        return str({name: value for name, value in instance.__dict__.items() if str(name) in fields})

