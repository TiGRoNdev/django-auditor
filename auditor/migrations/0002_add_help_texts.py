from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auditor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditlog',
            name='action',
            field=models.CharField(choices=[('SAVE', 'SAVE'), ('DELETE', 'DELETE'), ('M2M_CHANGE', 'M2M_CHANGE')], help_text='Type of the event', max_length=16),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='app_name',
            field=models.CharField(help_text='Name of application where is the audited model', max_length=255),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='date',
            field=models.DateTimeField(auto_now_add=True, help_text='Date when the changes were created'),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='model_name',
            field=models.CharField(help_text='Name of audited model', max_length=255),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='prev_state',
            field=models.TextField(help_text='All audit fields of concrete model in json format'),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='table_name',
            field=models.CharField(help_text='Name of table in db where is the audited model', max_length=255),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='username',
            field=models.CharField(db_index=True, help_text='Name of user who did this tracked changes', max_length=255),
        ),
    ]
