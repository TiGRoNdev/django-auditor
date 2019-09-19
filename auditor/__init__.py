"""
This app is needed for easy track/audit your Django-models

    You need to modify these files:

    tool/tool/wsgi.py
    .........................
    .    # your code
    .
    .    from auditor import AuditorAdmin
    .
    .    AuditorAdmin.setup()
    .........................


    tool/tool/settings.py
    .........................
    .   # your code
    .
    .   APPS_TO_AUDIT = [
    .       'my_app_with_models_to_audit',
    .       'my_second_app',
    .       ...
    .   ]
    .........................


    tool/tool_app/models.py
    .........................
    .   # your code before models
    .
    .   from auditor import audit
    .
    .   # if you need a model to audit do the next
    .
    .   @audit(**kwargs)
    .   class SomeModel(models.Model):
    .       # your code
    .
    .........................

    And also if you need more performance -> add to the following settings of celery(CELERY_BEAT_SCHEDULE)

    .......
    .. from auditor import AUDITOR_CELERY_BEAT_SCHEDULE
    .......

.. moduleauthor:: Igor Nazarov <tigron.dev@gmail.com>

"""

from .settings import AUDITOR_CELERY_BEAT_SCHEDULE
from .decorators import audit
from .apps import AuditorAdmin

__all__ = ('audit', 'AuditorAdmin', 'AUDITOR_CELERY_BEAT_SCHEDULE')

default_app_config = 'dm_tools_kit_common.django.apps.auditor.apps.AuditorAppConfig'
