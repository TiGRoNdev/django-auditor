from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auditor', '0003_auditlog_object_pk'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditServiceInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(help_text='Application name', max_length=255, serialize=False)),
                ('registered_model', models.CharField(help_text='Name of registered in the auditor model', max_length=255)),
                ('storage_depth', models.DurationField(help_text='Depth of storing history in timedelta')),
            ],
            options={
                'db_table': 'audit_service_info',
            },
        ),
        migrations.AlterUniqueTogether(
            name='auditserviceinfo',
            unique_together={('app', 'registered_model')},
        ),
    ]
