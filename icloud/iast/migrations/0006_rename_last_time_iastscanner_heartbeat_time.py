# Generated by Django 5.0 on 2024-03-02 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iast', '0005_iastscanner_last_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='iastscanner',
            old_name='last_time',
            new_name='heartbeat_time',
        ),
    ]
