# Generated by Django 5.0 on 2024-03-02 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iast', '0002_alter_flow_scan_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='IastScanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.CharField(max_length=128)),
                ('url', models.CharField(max_length=255)),
                ('create_time', models.IntegerField()),
            ],
            options={
                'db_table': 'icloud_iast_scanner',
            },
        ),
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('app_id', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=63)),
                ('description', models.CharField(max_length=255)),
                ('create_time', models.IntegerField()),
                ('config_time', models.IntegerField()),
                ('general_config', models.TextField()),
                ('whitelist_config', models.TextField()),
                ('selected_plugin_id', models.CharField(max_length=255)),
                ('algorithm_config', models.TextField()),
            ],
            options={
                'db_table': 'icloud_iast_strategy',
            },
        ),
    ]
