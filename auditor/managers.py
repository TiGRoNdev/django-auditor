"""
This default module contains managers for models in django-auditor.models

.. moduleauthor:: Igor Nazarov <tigron.dev@gmail.com>

"""
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db import models
import logging

from .const import SAVE
from .utils import is_equivalent


class AuditManager(models.Manager):
    """Manager for AuditLog model"""

    def create_record(self, action, username, instance, sender, fields):
        """Create one record for an one change of model instance

        Args:
            action: One of ACTION_CHOICES in django-auditor.const
            username: Name of user who did something that we tracking
            instance: Current(new) instance of model
            sender: The model which send signal to us
            fields: All field-names which we must audit

        Returns:
            New instance of AuditLog model
        """

        # get names of User's Django-app and Django-model
        app_name, model_name = instance._meta.label.split('.')

        # avoid any record creating in test mode
        if settings.TESTING:
            return

        try:
            # get name of column in table which is primary key for this model
            table_pk = instance._meta.pk.name
            # get current value by this column(primary key)
            table_pk_value = instance.__dict__[table_pk]
            # get current instance of model
            prev_instance = sender.objects.get(**{table_pk: table_pk_value})  # for dynamic column name
        except ObjectDoesNotExist as e:
            # this instance is being created and not updated. ignore and return
            logging.getLogger("info_logger").info("Signals: creating new instance of " + str(sender))
            return

        if action == SAVE:
            if is_equivalent(prev_instance, instance, fields=fields):
                logging.getLogger("info_logger").info("Signals: New instance hasn't diffs")
                return

        # create new record
        return self.create(
            username=username,
            app_name=app_name,
            model_name=model_name,
            table_name=str(instance._meta.db_table),
            action=action,
            object_pk=str(table_pk_value),
            prev_state=prev_instance.auditor_to_raw_json(fields)
            # Get previous instance in raw JSON-string
        )
