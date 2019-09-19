from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auditor', '0004_auto_20190320_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditserviceinfo',
            name='app',
            field=models.CharField(help_text='Application name', max_length=255),
        ),
    ]
