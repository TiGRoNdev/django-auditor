from django.apps import apps, AppConfig
from django.conf import settings


class AuditorAdmin:
    """Manager for responsible service commands"""

    class Model:
        """Commands for model management"""

        AUDITED_MODEL_FIELDS = ['auditor_to_raw_json', 'get_audited_log', 'auditor_storage_depth']

        @classmethod
        def register(cls, unregistered_model):
            """
            Args:
                unregistered_model: django model to registration
            """
            from .models import AuditServiceInfo

            AuditServiceInfo.objects.create(
                app=unregistered_model._meta.app_label,
                registered_model=unregistered_model._meta.object_name,
                storage_depth=unregistered_model.auditor_storage_depth
            )

        @classmethod
        def ready_for_register(cls, django_model):
            """
            Args:
                django_model: model for checking if its ready to register
            """
            from .models import AuditServiceInfo

            return (
                all([hasattr(django_model, attr) for attr in cls.AUDITED_MODEL_FIELDS]) and
                not AuditServiceInfo.objects.filter(
                    app=django_model._meta.app_label,
                    registered_model=django_model._meta.object_name
                ).exists()
            )

    class App:
        """Commands for app management"""

        @classmethod
        def ready_for_audit(cls, app_label):
            """
            Args:
                app_label: name of app which we need to check for its ready or
                    not
            """
            django_models = []

            if apps.is_installed(app_label):
                django_models = apps.get_app_config(app_label).get_models()

            return [
                django_model
                for django_model in django_models
                if AuditorAdmin.Model.ready_for_register(django_model)
            ]

    @classmethod
    def setup(cls):
        
        if settings.TESTING or not hasattr(settings, 'APPS_TO_AUDIT'):
            return

        unregistered_models = []
        ready_models_by_app = [
            cls.App.ready_for_audit(app_label)
            for app_label in settings.APPS_TO_AUDIT
        ]

        for ready_models in ready_models_by_app:
            unregistered_models.extend(ready_models)

        for unregistered_model in unregistered_models:
            cls.Model.register(unregistered_model)

        return unregistered_models, ready_models_by_app


class AuditorAppConfig(AppConfig):
    name = 'dm_tools_kit_common.django.apps.auditor'
    verbose_name = "Django Auditor app"


