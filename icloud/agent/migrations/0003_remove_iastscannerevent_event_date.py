# Generated by Django 5.0 on 2024-03-08 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0002_iastscannerevent_event_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iastscannerevent',
            name='event_date',
        ),
    ]