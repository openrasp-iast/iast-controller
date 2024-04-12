import hashlib
import uuid
from django.db import models

from controller.models import App


# Create your models here.
class Rasp(models.Model):
    """
    type Rasp struct {
            Id                string            `json:"id" bson:"_id,omitempty"`
            AppId             string            `json:"app_id" bson:"app_id,omitempty"`
            StrategyId        string            `json:"strategy_id" bson:"strategy_id,omitempty"`
            Version           string            `json:"version" bson:"version,omitempty"`
            Os                string            `json:"os" bson:"os,omitempty"`
            HostName          string            `json:"hostname" bson:"hostname,omitempty"`
            RegisterIp        string            `json:"register_ip" bson:"register_ip,omitempty"`
            Language          string            `json:"language" bson:"language,omitempty"`
            LanguageVersion   string            `json:"language_version" bson:"language_version,omitempty"`
            ServerType        string            `json:"server_type" bson:"server_type,omitempty"`
            ServerVersion     string            `json:"server_version" bson:"server_version,omitempty"`
            RaspHome          string            `json:"rasp_home" bson:"rasp_home,omitempty"`
            PluginVersion     string            `json:"plugin_version" bson:"plugin_version,omitempty"`
            PluginName        string            `json:"plugin_name" bson:"plugin_name,omitempty"`
            PluginMd5         string            `json:"plugin_md5" bson:"plugin_md5,omitempty"`
            HostType          string            `json:"host_type" bson:"host_type,omitempty"`
            HeartbeatInterval int64             `json:"heartbeat_interval" bson:"heartbeat_interval,omitempty"`
            Online            *bool             `json:"online" bson:"online,omitempty"`
            LastHeartbeatTime int64             `json:"last_heartbeat_time" bson:"last_heartbeat_time,omitempty"`
            RegisterTime      int64             `json:"register_time" bson:"register_time,omitempty"`
            Environ           map[string]string `json:"environ" bson:"environ,omitempty"`
            Description       string            `json:"description" bson:"description,omitempty"`
            HostNameList      []string          `json:"hostname_list" bson:"hostname_list,omitempty"`
    }
    """

    id = models.CharField(max_length=255, primary_key=True)
    app_id = models.ForeignKey(App, on_delete=models.CASCADE)
    strateg_id = models.CharField(max_length=255)
    selected_plugin_id = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    register_ip = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    language_version = models.CharField(max_length=255)
    server_type = models.CharField(max_length=255)
    server_version = models.CharField(max_length=255)
    rasp_home = models.CharField(max_length=255)
    plugin_version = models.CharField(max_length=255)
    plugin_name = models.CharField(max_length=255)
    plugin_md5 = models.CharField(max_length=255)
    host_type = models.CharField(max_length=255, null=True, blank=True)
    heartbeat_interval = models.IntegerField()
    online = models.BooleanField(default=True)
    last_heartbeat_time = models.BigIntegerField(null=True, blank=True)
    register_time = models.BigIntegerField(null=True, blank=True)
    environ = models.JSONField(null=True, blank=True)
    description = models.TextField()
    hostname_list = models.JSONField(null=True, blank=True)


class Plugin(models.Model):
    """
    type Plugin struct {
        Id                     string                 `json:"id" bson:"_id,omitempty"`
        AppId                  string                 `json:"app_id" bson:"app_id"`
        Name                   string                 `json:"name" bson:"name"`
        UploadTime             int64                  `json:"upload_time" bson:"upload_time"`
        Version                string                 `json:"version" bson:"version"`
        Description            string                 `json:"description" bson:"description"`
        Md5                    string                 `json:"md5" bson:"md5"`
        OriginContent          string                 `json:"origin_content,omitempty" bson:"origin_content"`
        Content                string                 `json:"plugin,omitempty" bson:"content"`
        DefaultAlgorithmConfig map[string]interface{} `json:"-" bson:"default_algorithm_config"`
        AlgorithmConfig        map[string]interface{} `json:"algorithm_config" bson:"algorithm_config"`
    }
    """

    id = models.CharField(max_length=128, primary_key=True)
    app_id = models.ForeignKey(App, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    upload_time = models.BigIntegerField()
    version = models.CharField(max_length=128)
    description = models.TextField()
    md5 = models.CharField(max_length=128)
    origin_content = models.TextField(null=True, blank=True)
    content = models.TextField()
    default_algorithm_config = models.JSONField(null=True, blank=True)
    algorithm_config = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            unique_id = uuid.uuid4().hex
            hashed_id = hashlib.sha256(unique_id.encode()).hexdigest()
            self.id = hashed_id

        super().save(*args, **kwargs)


class Dependency(models.Model):
    """
    type Dependency struct {
        Path         []string `json:"path"`
        CreateTime   int64    `json:"@timestamp"`
        RaspId       string   `json:"rasp_id"`
        HostName     string   `json:"hostname"`
        RegisterIp   string   `json:"register_ip"`
        AppId        string   `json:"app_id"`
        Vendor       string   `json:"vendor"`
        Product      string   `json:"product"`
        Version      string   `json:"version"`
        Tag          string   `json:"tag"`
        SearchString string   `json:"search_string"`
        Source       string   `json:"source"`
    }
    """

    app_id = models.ForeignKey(App, on_delete=models.CASCADE)
    rasp_id = models.ForeignKey(Rasp, on_delete=models.CASCADE)

    path = models.JSONField(null=True, blank=True)
    create_time = models.BigIntegerField(null=True, blank=True)
    hostname = models.CharField(max_length=255, null=True, blank=True)
    register_ip = models.CharField(max_length=32, null=True, blank=True)
    vendor = models.CharField(max_length=255, null=True, blank=True)
    product = models.CharField(max_length=255, null=True, blank=True)
    version = models.CharField(max_length=255, null=True, blank=True)
    tag = models.CharField(max_length=255, null=True, blank=True)
    search_string = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)


class IastScannerEvent(models.Model):
    vuln_id = models.CharField(max_length=128)
    rasp_id = models.CharField(max_length=20)
    app_id = models.CharField(max_length=50)
    event_type = models.CharField(max_length=20)
    event_time = models.CharField(max_length=50)
    event_date = models.DateField(null=True, blank=True)
    request_id = models.CharField(max_length=64, null=True, blank=True)
    request_method = models.CharField(max_length=10)
    intercept_state = models.CharField(max_length=10)
    vuln_state = models.CharField(max_length=10, null=True, blank=True)
    target = models.CharField(max_length=255)
    server_hostname = models.CharField(max_length=255)
    server_ip = models.CharField(max_length=128)
    server_type = models.CharField(max_length=50)
    server_version = models.CharField(max_length=50)
    server_nic = models.JSONField(max_length=255)
    path = models.CharField(max_length=255)
    url = models.URLField()
    attack_type = models.CharField(max_length=50)
    attack_type_name = models.CharField(max_length=50, null=True, blank=True)
    attack_params = models.JSONField()
    attack_source = models.CharField(max_length=128)
    client_ip = models.CharField(max_length=128)
    plugin_name = models.CharField(max_length=50)
    plugin_confidence = models.IntegerField()
    plugin_message = models.TextField()
    plugin_algorithm = models.TextField()
    header = models.JSONField()
    stack_trace = models.TextField()
    body = models.TextField()
    count = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.vuln_id:
            unique_id = uuid.uuid4().hex
            hashed_id = hashlib.sha256(unique_id.encode()).hexdigest()
            self.vuln_id = hashed_id

        super().save(*args, **kwargs)

    class Meta:
        db_table = "icloud_iast_vuln"
        unique_together = ("rasp_id", "request_id")
