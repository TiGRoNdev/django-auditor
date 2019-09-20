# django-auditor
This app is needed for easy track/audit your Django-models


## Getting started

You need to modify these files in your project *tool* with inner django app *tool_app*:

#### tool/tool/wsgi.py
```python
from auditor import AuditorAdmin
  
# your code with wsgi app
  
AuditorAdmin.setup()
```

#### tool/tool/settings.py
```python
# your code
  
INSTALLED_APPS = [
    'tool_app',
    'auditor',
    ...
]

APPS_TO_AUDIT = [
    'my_app_with_models_to_audit',
    'my_second_app',
    ...
]
```


#### tool/tool_app/models.py
```python
import datetime
from auditor import audit

# if you need a model to audit do the next

# storage_depth is a time for store logs, it's not required
@audit(storage_depth=datetime.timedelta(weeks=12), **kwargs)  
class SomeModel(models.Model):
    field1 = models.CharField(...)  # example field
    field2 = models.BooleanField(...)  # example field
    # your code of model
```

And also if you need more performance then add to the following settings of celery(CELERY_BEAT_SCHEDULE)
```python
from auditor import AUDITOR_CELERY_BEAT_SCHEDULE
```

## Intro
Now you're ready to audit all of changes in your Django-models, also you can access to the audited log of model:
```python
SomeModel.get_audited_log(pk, limit=100)  # returns 100 last audit records of SomeModel object with primary key = pk

# the solution for a django-rest-framework's ModelViewSet, example is below
from auditor.rest_framework import AuditModelViewSetMixin

class ExampleViewSet(viewsets.ModelViewSet, AuditModelViewSetMixin):  # now it defines a GET handler to .../pk/audited_log
    authentication_classes = [DMUserAuthentication, BasicAuthentication]

    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    queryset = Example.objects.all()
    serializer_class = ExampleSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'id',
        'name',
        'description'
    )

```
