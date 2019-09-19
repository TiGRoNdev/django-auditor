from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auditor', '0002_add_help_texts'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditlog',
            name='object_pk',
            field=models.CharField(default="1", help_text='PK of instance which is audited', max_length=255),
            preserve_default=False,
        ),
    ]
