import datetime
import hashlib
import json

from ninja import File, Router, UploadedFile
from django.core.paginator import Paginator
from django.forms.models import model_to_dict

from agent.models import Plugin
from controller.models import App
from controller.schemas import PluginFilterSchema, PluginSchema

import structlog


logger = structlog.get_logger(__name__)

router = Router()


@router.post("/")
def plugin(request, file: UploadedFile, app_id: str):
    """
    描述：上传文件为 .js 结尾的插件文件，插件版本在文件第一行，插件名称在插件的第二行

    Args:
        request (_type_): _description_
        app_id (str): _description_

    Returns:
        _type_: _description_
    """
    logger.info(app_id)
    logger.info(">>>>>>>>>>>>>>>>", javascript=file)

    app = App.objects.get(id=app_id)

    # 初始化 MD5 计算
    md5_hash = hashlib.md5()

    # 初始化用于存储关键信息的变量
    plugin_version = None
    plugin_name = None
    plugin_desc = None

    # 逐行读取文件
    content = ""
    for line in file:
        # 更新 MD5
        md5_hash.update(line)

        # content
        content += line.decode()

        # 检查并提取需要的信息
        if line.startswith(b"const plugin_version ="):
            plugin_version = line.decode().split("'")[1]
        elif line.startswith(b"const plugin_name ="):
            plugin_name = line.decode().split("'")[1]
        elif line.startswith(b"const plugin_desc ="):
            plugin_desc = line.decode().split("'")[1]

    md5_digest = md5_hash.hexdigest()
    if Plugin.objects.filter(md5=md5_digest).exists():
        return {
            "status": -1,
            "description": "same md5",
            "data": {},
        }

    plugin = Plugin()
    plugin.app_id = app
    plugin.name = plugin_name
    plugin.version = plugin_version
    plugin.description = plugin_desc
    plugin.md5 = md5_digest
    plugin.content = content
    plugin.upload_time = int(datetime.datetime.now().timestamp())
    plugin.default_algorithm_config = json.dumps(
        {
            "iast": {
                "byhost_regex": ".*",
                "fuzz_server": "http://127.0.0.1:8080/v1/iast/flow",
                "request_timeout": 5000,
            },
            "meta": {},
        }
    )
    if not plugin.algorithm_config:
        plugin.algorithm_config = plugin.default_algorithm_config
    plugin.save()

    return {
        "data": {**model_to_dict(plugin)},
        "description": "ok",
        "status": 0,
    }


@router.get("/download")
def download(request, id: str):
    return {"返回结果 ：插件文件，文件名称为 {NAME}-{VERSION}.js，{VERSION} 为插件版本，{NAME}为插件名称"}


@router.post("/get")
def get_plugin(request, body: PluginFilterSchema):
    if body.plugin_id:
        try:
            plugin = Plugin.objects.get(id=body.plugin_id)
            return {"status": 0, "description": "ok", "data": model_to_dict(plugin)}
        except Plugin.DoesNotExist:
            return {"status": -1, "description": "plugin not found"}

    # lookup by plugin_name 模糊查询
    if body.plugin_name:
        plugins = Plugin.objects.filter(name__icontains=body.plugin_name)
    else:
        plugins = Plugin.objects.all()

    page = body.page or 1
    perpage = body.perpage or 5

    # 创建一个Paginator对象，每页显示10个对象
    paginator = Paginator(plugins, perpage)

    # 获取第一页的内容
    plugins = [model_to_dict(plugin) for plugin in paginator.page(page).object_list]

    return {
        "status": 0,
        "description": "ok",
        "data": plugins,
        "total": paginator.count,
        "page": page,
        "perpage": perpage,
    }


@router.post("/save")
def save_plugin(request, body: PluginSchema):
    logger.debug(body)

    if Plugin.objects.filter(id=body.plugin_id).exists():
        algorithm_config = {
            "iast": {
                "fuzz_server": body.fuzz_server,
                "request_timeout": body.request_timeout,
                "byhost_regex": body.byhost_regex,
            },
            "meta": {},
        }
        plugin = Plugin.objects.get(id=body.plugin_id)
        plugin.algorithm_config = algorithm_config
        plugin.save()
        logger.debug("save plugin success")

        return {"status": 0, "description": "ok"}
    else:
        return {"status": -1, "description": "plugin not found"}


@router.post("/delete")
def delete_plugin(request, body: PluginFilterSchema):
    logger.debug(body)

    if Plugin.objects.filter(id=body.plugin_id).exists():
        Plugin.objects.get(id=body.plugin_id).delete()
        return {"status": 0, "description": "ok"}
    else:
        return {"status": -1, "description": "plugin not found"}
