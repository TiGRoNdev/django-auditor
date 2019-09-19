"""
This module contains all receivers for Django-signals

.. moduleauthor:: Igor Nazarov <tigron.dev@gmail.com>

"""
from .utils import get_current_authenticated_user
from .models import AuditLog


def create_receiver(action_type, fields):
    """
    Creates specialized receiver for a concrete model.

    :param action_type: One of event types from django-auditor.const
    :param fields: List of field names to audit
    :return: New specialized receiver
    """
    def receiver(sender, instance, **kwargs):
        """
        Receiver which will be catch all django-signals from sender model

        :param sender: Django-Model class
        :param instance: instance(of Django-Model class) which did something on
        :param kwargs: something params
        :return: Nothing
        """

        # get current user from local thread
        current_user = get_current_authenticated_user()
        if not current_user:
            username = 'anonymous'
        else:
            username = current_user.username

        # create new record in audit_log table
        AuditLog.objects.create_record(action_type, username, instance, sender, fields)

    return receiver
