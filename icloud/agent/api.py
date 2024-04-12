import datetime
import json
import time
from django.forms import model_to_dict
from django.db.models import Q
from django.http import HttpRequest
from ninja import Router
from ninja.security import APIKeyHeader
from agent.routers.log import router as log_router
from agent.models import Dependency, Plugin, Rasp
from agent.schemas import Dependencies, Heartbeat, RaspSchema, Report

from controller.models import App

import structlog

logger = structlog.get_logger(__name__)


class ApiKey(APIKeyHeader):
    param_name = "X-OpenRASP-AppSecret"

    def authenticate(self, request, secret):
        app_id = request.headers.get("X-OpenRASP-AppID")

        # 判断数据库表 App 中是否存在 app_id 和 secret 的记录
        if App.objects.filter(id=app_id, secret=secret).exists():
            return app_id
        return None


router = Router(auth=ApiKey())
router.add_router("log", log_router)


@router.post("/rasp")
def rasp(request, body: RaspSchema):
    app_id = request.headers.get("X-OpenRASP-AppID")
    app = App.objects.get(id=app_id)

    if not Rasp.objects.filter(id=body.id).exists():
        rasp = Rasp(**body.dict())
        rasp.app_id = app
        rasp.register_time = int(time.time())

    else:
        rasp = Rasp.objects.get(id=body.id)

    rasp.last_heartbeat_time = int(time.time())
    rasp.save()

    return {
        "status": 0,
        "description": "ok",
        "data": {**model_to_dict(rasp)},
    }


@router.post("/report")
def report(request, body: Report):
    # TODO
    logger.info(body)
    return {"status": 0, "description": "ok", "data": {}}


@router.post("/heartbeat")
def heartbeat(request: HttpRequest, body: Heartbeat):
    """
    plugin	    插件内容
    config_time	本次下发配置的时间
    config	    下发的配置，配置项的详细说明：https://rasp.baidu.com/doc/setup/others.html
    rasp_id='4d8d020f1abc92939c5ac3c0be54221b' plugin_md5='' plugin_version='' config_time=1706335369 hostname='sec'
    """
    logger.info(body)

    # 获取当前 RASP 对象
    try:
        rasp = Rasp.objects.get(id=body.rasp_id)
    except Rasp.DoesNotExist:
        return {"status": 1, "description": "rasp not found", "data": {}}

    # 刷新通信时间
    rasp.last_heartbeat_time = int(datetime.datetime.now().timestamp())
    rasp.save()

    # 获取应用选择的插件
    if (
        rasp.selected_plugin_id
        and Plugin.objects.filter(id=rasp.selected_plugin_id).exists()
    ):
        plugin = Plugin.objects.get(id=rasp.selected_plugin_id)
    else:
        # 获取第一个插件作为默认选择插件
        plugin = Plugin.objects.first()
        if not plugin:
            return {"status": 1, "description": "plugin not found", "data": {}}
        rasp.selected_plugin_id = plugin.id
        rasp.save()

    if plugin.md5 == body.plugin_md5:
        data = {}
    else:
        # 1.更新 RASP
        rasp.plugin_name = plugin.name
        rasp.plugin_version = plugin.version
        rasp.plugin_md5 = plugin.md5
        rasp.save()

        # 2.返回 Plugin
        data = {
            "plugin": {
                "name": plugin.name,
                "version": plugin.version,
                "md5": plugin.md5,
                "plugin": plugin.content.replace(
                    "http://127.0.0.1:8080/v1/iast/flow",
                    (
                        plugin.algorithm_config["iast"]["fuzz_server"]
                        if type(plugin.algorithm_config) == dict
                        else json.loads(plugin.algorithm_config)["iast"]["fuzz_server"]
                    ),
                ),
            },
            "config_time": int(datetime.datetime.now().timestamp()),
            "config": plugin.algorithm_config,
        }

    return {"status": 0, "description": "ok", "data": data}


@router.post("/dependency")
def dependency(request, body: Dependencies):
    app_id = request.headers.get("X-OpenRASP-AppID")
    app = App.objects.get(id=app_id)

    rasp = Rasp.objects.get(app_id=app_id)

    for dep in body.dependency:
        if not Dependency.objects.filter(
            Q(product=dep.product)
            & Q(vendor=dep.vendor)
            & Q(version=dep.version)
            & Q(source=dep.source)
            & Q(path=dep.path)
        ).exists():
            dependency = Dependency(**dep.dict())
            dependency.app_id = app
            dependency.rasp_id = rasp
            dependency.create_time = int(datetime.datetime.now().timestamp())
            dependency.save()
    return {"status": 0, "description": "ok", "data": {}}
