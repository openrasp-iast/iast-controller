import hashlib
import uuid
from django.db import models


# Create your models here.
class Flow(models.Model):
    """
    +-------------+-------------+------+-----+---------+----------------+
    | Field       | Type        | Null | Key | Default | Extra          |
    +-------------+-------------+------+-----+---------+----------------+
    | id          | int         | NO   | PRI | NULL    | auto_increment |
    | data        | longtext    | NO   |     | NULL    |                |
    | data_hash   | varchar(63) | NO   | UNI | NULL    |                |
    | scan_status | int         | NO   |     | NULL    |                |
    | time        | int         | NO   |     | NULL    |                |
    +-------------+-------------+------+-----+---------+----------------+

    TODO 新增 [ 'Host': '192.168.106.26:8080' ] 字段，标明数据流的来，方便分布式扫描器区分扫描
    """

    data = models.TextField()
    data_hash = models.CharField(max_length=63, unique=True)
    scan_status = models.BooleanField(default=False)  # 改进
    time = models.IntegerField()

    class Meta:
        db_table = "icloud_iast_flow"


class Report(models.Model):
    """
    +------------------+-------------+------+-----+---------+----------------+
    | Field            | Type        | Null | Key | Default | Extra          |
    +------------------+-------------+------+-----+---------+----------------+
    | id               | int         | NO   | PRI | NULL    | auto_increment |
    | plugin_name      | varchar(63) | NO   |     | NULL    |                |
    | description      | text        | NO   |     | NULL    |                |
    | rasp_result_list | longtext    | NO   |     | NULL    |                |
    | payload_seq      | varchar(63) | NO   | UNI | NULL    |                |
    | message          | text        | NO   |     | NULL    |                |
    | time             | int         | NO   |     | NULL    |                |
    | upload           | int         | NO   |     | NULL    |                |
    +------------------+-------------+------+-----+---------+----------------+

    """

    plugin_name = models.CharField(max_length=63)
    description = models.TextField()
    rasp_result_list = models.TextField()
    payload_seq = models.CharField(max_length=63, unique=True)
    message = models.TextField()
    time = models.IntegerField()
    upload = models.IntegerField()

    class Meta:
        db_table = "icloud_iast_report"


class Strategy(models.Model):
    """
    扫描策略

    type Strategy struct {
        Id               	string                 `json:"id" bson:"_id"`
        AppId				string				   `json:"app_id" bson:"app_id"`
        Name             	string                 `json:"name"  bson:"name"`
        Description      	string                 `json:"description"  bson:"description"`
        CreateTime       	int64                  `json:"create_time"  bson:"create_time"`
        ConfigTime       	int64                  `json:"config_time"  bson:"config_time"`
        GeneralConfig   	map[string]interface{} `json:"general_config"  bson:"general_config"`
        WhitelistConfig  	[]WhitelistConfigItem  `json:"whitelist_config"  bson:"whitelist_config"`
        SelectedPluginId 	string                 `json:"selected_plugin_id" bson:"selected_plugin_id"`
        AlgorithmConfig     map[string]interface{} `json:"algorithm_config"`
    }
    """

    id = models.CharField(max_length=255, primary_key=True)
    app_id = models.CharField(max_length=128)
    name = models.CharField(max_length=63)
    description = models.CharField(max_length=255)
    create_time = models.IntegerField()
    config_time = models.IntegerField()
    general_config = models.TextField()
    whitelist_config = models.TextField()
    selected_plugin_id = models.CharField(max_length=255)
    algorithm_config = models.TextField()

    def save(self, *args, **kwargs):
        if not self.id:
            unique_id = uuid.uuid4().hex
            hashed_id = hashlib.sha256(unique_id.encode()).hexdigest()
            self.id = hashed_id

        super().save(*args, **kwargs)

    class Meta:
        db_table = "icloud_iast_strategy"


class IastScanner(models.Model):
    """
    iast-scanner
    """

    app_id = models.CharField(max_length=128)
    url = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    heartbeat_time = models.IntegerField(default=0)

    class Meta:
        db_table = "icloud_iast_scanner"
        unique_together = ("app_id", "url")
