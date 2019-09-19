"""
This module contains the main decorator 'audit' for models.Model by Django and many others

.. moduleauthor:: Igor Nazarov <tigron.dev@gmail.com>

"""
import re
import datetime  # for eval
from django.db.models import signals

from .utils import auditor_to_raw_json

from .models import AuditLog

from .receivers import create_receiver
from .const import SAVE, DELETE, M2M_CHANGE


def get_audited_log(cls, pk, limit=100):
    """Returns audited log of target instance with some limit. If limit equal to
    0 that the response log will be unlimited and full

    Args:
        cls: Django-model class
        pk (int): Primary Key value
        limit (int): count of objects in result list

    Returns:
        list of last audited events on target instance sorted by date from lower
        to upper
    """
    # get names of User's Django-app and Django-model
    app_name, model_name = cls._meta.label.split('.')

    filtered_log = AuditLog.objects.filter(
        app_name=app_name,
        model_name=model_name,
        object_pk=str(pk)
    )

    return list(map(
        lambda audited_log: {
            **audited_log,
            "prev_state": dict(eval(
                re.sub(r', tzinfo=<\w+>\)', ')', audited_log["prev_state"])
                # replace tzinfo with empty cause of syntax error
            ))
        },

        filtered_log.order_by('-date')[:limit].values()
        if limit != 0 else
        filtered_log.order_by('-date').values()
    ))


def audit(fields=[], options=[], storage_depth=datetime.timedelta(weeks=12)):
    """Decorator for Django-model

    Args:
        fields (list): List of field-names to audit and it become to all fields
            if not provided
        options (list): List of event types to audit, audit all types if empty
        storage_depth (datetime.timedelta): Time of storing
            model's history in db

    Returns:
        django.db.models.Model: decorated Django-model
    """
    if len(options) == 0:
        options = [SAVE, DELETE, M2M_CHANGE]

    def wrap(cls):
        # set serialize function to Django-model class
        setattr(cls, 'auditor_to_raw_json', auditor_to_raw_json)
        # set view function to get all history of target object
        setattr(cls, 'get_audited_log', classmethod(get_audited_log))
        # set storage depth param for right resolving if we wanna to delete retro data
        setattr(cls, 'auditor_storage_depth', storage_depth)

        # create receiver for something signal, then connect class and receiver to django signals
        if SAVE in options:
            signals.pre_save.connect(receiver=create_receiver(SAVE, fields), sender=cls, weak=False)
        if DELETE in options:
            signals.pre_delete.connect(receiver=create_receiver(DELETE, fields), sender=cls, weak=False)
        if M2M_CHANGE in options:
            signals.m2m_changed.connect(receiver=create_receiver(M2M_CHANGE, fields), sender=cls, weak=False)

        return cls

    return wrap
