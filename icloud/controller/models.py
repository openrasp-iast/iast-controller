from django.db import models

from controller.util.app_util import generate_app_id, generate_secret


class App(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    language = models.CharField(max_length=100)
    description = models.TextField()
    #
    create_time = models.DateTimeField(auto_now_add=True)
    config_time = models.DateTimeField(auto_now_add=True)
    selected_plugin_id = models.CharField(max_length=255)
    #
    general_config = models.JSONField(null=True, blank=True)
    whitelist_config = models.JSONField(null=True, blank=True)
    attack_type_alarm_conf = models.JSONField(null=True, blank=True)
    email_alarm_conf = models.JSONField(null=True, blank=True)
    ding_alarm_conf = models.JSONField(null=True, blank=True)
    http_alarm_conf = models.JSONField(null=True, blank=True)
    algorithm_config = models.JSONField(null=True, blank=True)
    general_alarm_conf = models.JSONField(null=True, blank=True)
    kafka_alarm_conf = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_app_id(self.name)
        if not self.secret:
            self.secret = generate_secret(self.name, self.id)

        super().save(*args, **kwargs)

    class Meta:
        db_table = "icloud_controller_app"


class Setting(models.Model):
    name = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "icloud_controller_setting"
