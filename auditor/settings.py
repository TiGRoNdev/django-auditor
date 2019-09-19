"""
There are celery settings for django-auditor app.

.. moduleauthor:: Igor Nazarov <tigron.dev@gmail.com>

"""
from celery.schedules import crontab

AUDITOR_CELERY_BEAT_SCHEDULE = {
    "auditor_delete_retro_data": {
        "task": "dm_tools_kit_common.django.apps.auditor.tasks.delete_retro_data",
        "schedule": crontab(day_of_week=2, hour=3)
    },
    "auditor_delete_untracked_data": {
        "task": "dm_tools_kit_common.django.apps.auditor.tasks.delete_untracked_records",
        "schedule": crontab(day_of_week=2, hour=3)
    }
}
