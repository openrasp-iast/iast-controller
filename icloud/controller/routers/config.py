from django.forms import model_to_dict
from ninja import Router

from controller.models import Setting
from controller.schemas import SettingFilterSchema, SettingSchema

import structlog

logger = structlog.get_logger(__name__)

router = Router()


@router.post("/save")
def save_config(request, body: SettingSchema):
    """
    保存设置
    """
    try:
        for key, value in body.dict().items():
            logger.info(f"{key}: {value}")
            option, created = Setting.objects.update_or_create(name=key)
            if created:
                option.name = key
            option.value = value
            option.save()
    except Exception as e:
        return {"status": 1, "description": str(e)}

    return {"status": 0, "description": "ok"}


@router.post("/get")
def get_config(request, body: SettingFilterSchema):
    """
    获取配置
    """
    try:
        if body.name_start_with:
            result = Setting.objects.filter(
                name__startswith=body.name_start_with
            ).values_list("name", "value")
            result_dict = {k: v for k, v in result}
            if result:
                return {
                    "status": 0,
                    "description": "ok",
                    "data": result_dict,
                }
    except Exception as e:
        return {"status": 1, "description": str(e)}

    return {"status": 0, "description": "ok", "data": []}
