# Generated by Django 5.0 on 2024-03-02 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iast', '0003_iastscanner_strategy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iastscanner',
            name='create_time',
        ),
        migrations.AddField(
            model_name='iastscanner',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
