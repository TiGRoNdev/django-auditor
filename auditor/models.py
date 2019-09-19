"""
This module contains Django-models which are storing all changes of decorated models

.. moduleauthor:: Igor Nazarov <tigron.dev@gmail.com>

"""
from django.db import models

from .const import ACTION_CHOICES
from .managers import AuditManager


class AuditServiceInfo(models.Model):
    """Store info about registered models and other stuff"""

    class Meta:
        app_label = 'auditor'
        db_table = 'audit_service_info'
        unique_together = ('app', 'registered_model')

    app = models.CharField(max_length=255, null=False,
                           help_text="Application name")

    registered_model = models.CharField(max_length=255, null=False,
                                        help_text="Name of registered in the auditor model")

    storage_depth = models.DurationField(null=False,
                                         help_text="Depth of storing history in timedelta")


class AuditLog(models.Model):
    """
    Store for all Model's changes.
    """

    class Meta:
        app_label = 'auditor'  # global application name
        db_table = 'audit_log'  # name of table in database

    username = models.CharField(max_length=255, null=False, db_index=True,
                                help_text="Name of user who did this tracked changes")

    app_name = models.CharField(max_length=255, null=False,
                                help_text="Name of application where is the audited model")

    model_name = models.CharField(max_length=255, null=False,
                                  help_text="Name of audited model")

    table_name = models.CharField(max_length=255, null=False,
                                  help_text="Name of table in db where is the audited model")

    object_pk = models.CharField(max_length=255, null=False,
                                 help_text="PK of instance which is audited")

    prev_state = models.TextField(null=False,
                                  help_text="All audit fields of concrete model in json format")

    action = models.CharField(max_length=16, null=False, choices=ACTION_CHOICES,
                              help_text="Type of the event")

    date = models.DateTimeField(null=False, auto_now_add=True,
                                help_text="Date when the changes were created")

    objects = AuditManager()
