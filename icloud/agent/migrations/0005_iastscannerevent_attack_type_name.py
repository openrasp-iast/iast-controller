# Generated by Django 5.0 on 2024-03-08 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0004_iastscannerevent_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='iastscannerevent',
            name='attack_type_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
