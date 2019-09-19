"""
There are celery tasks for django-auditor app.

.. moduleauthor:: Igor Nazarov <tigron.dev@gmail.com>

"""
from __future__ import absolute_import, unicode_literals
import logging
from django.utils import timezone
from collections import defaultdict
from celery import shared_task

from .models import AuditServiceInfo, AuditLog

logger = logging.getLogger(__name__)


@shared_task
def delete_retro_data():
    records_to_delete_qs = AuditLog.objects.filter(id__lt=2) & AuditLog.objects.filter(id__gt=3)  # empty QS
    result = defaultdict(dict)

    for tracked_model in AuditServiceInfo.objects.all():
        qs = AuditLog.objects.filter(
            app_name=tracked_model.app,
            model_name=tracked_model.registered_model,
            date__lt=timezone.now() - tracked_model.storage_depth
        )

        if not qs.exists():
            qs = AuditLog.objects.filter(
                app_name=tracked_model.app,
                model_name=tracked_model.registered_model
            ).order_by('date')

            result[f"{tracked_model.app}.{tracked_model.registered_model}"] = {
                "oldest": str(qs.first().date) if qs.exists() else None,
            }

            continue

        result[f"{tracked_model.app}.{tracked_model.registered_model}"] = {
            "oldest": str(qs.order_by('date').first().date),
            "newest": str(qs.order_by('date').last().date),
            "count": qs.count()
        }
        records_to_delete_qs = records_to_delete_qs | qs

    result["count_sum"] = records_to_delete_qs.count()

    records_to_delete_qs.delete()

    return result


@shared_task
def delete_untracked_records():
    result = defaultdict(list)

    untracked_records_qs = AuditLog.objects.all()
    for tracked_model in AuditServiceInfo.objects.all():
        if untracked_records_qs.filter(
                app_name=tracked_model.app,
                model_name=tracked_model.registered_model
        ).exists():
            result["exist"].append(f"{tracked_model.app}.{tracked_model.registered_model}")

        untracked_records_qs = untracked_records_qs.exclude(
            app_name=tracked_model.app,
            model_name=tracked_model.registered_model
        )

    if not untracked_records_qs.exists():
        result["deleted"] = []
        return result

    result["deleted"].extend([
        {
            "model": f"{untracked_model['app_name']}.{untracked_model['model_name']}",
            "count": untracked_records_qs.filter(**untracked_model).count()
        }
        for untracked_model in untracked_records_qs.values('app_name', 'model_name').distinct()
    ])

    untracked_records_qs.delete()

    return result

