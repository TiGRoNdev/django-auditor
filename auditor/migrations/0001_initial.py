from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(db_index=True, max_length=255)),
                ('app_name', models.CharField(max_length=255)),
                ('model_name', models.CharField(max_length=255)),
                ('table_name', models.CharField(max_length=255)),
                ('prev_state', models.TextField()),
                ('action', models.CharField(choices=[('SAVE', 'SAVE'), ('DELETE', 'DELETE'), ('M2M_CHANGE', 'M2M_CHANGE')], max_length=16)),
                ('date', models.DateTimeField()),
            ],
            options={
                'db_table': 'audit_log',
            },
        ),
    ]
