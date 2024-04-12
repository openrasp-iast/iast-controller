import datetime
from ninja import Router

from iast.schemas import TargetFilterSchema
from iast.services.iast_api_service import (
    service_clean_target,
    service_get_target,
    service_new_or_start_target,
    service_stop_scanning_target,
)
from iast.models import IastScanner

import structlog


logger = structlog.get_logger(__name__)

router = Router()


@router.post("/target")
def get_target(request, body: TargetFilterSchema):
    logger.debug(body)
    if not body.app_id:
        return {
            "status": 1,
            "description": "app_id does not exist.",
            "data": [],
        }
    # 根据 body.app_id 查询iast扫描器监听接口地址
    try:
        iast_scanner = IastScanner.objects.get(app_id=body.app_id)
        iast_scanner_url = iast_scanner.url

        # 如果状态为假或者超时，直接返回
        if (
            not iast_scanner.status
            or iast_scanner.heartbeat_time
            < int(datetime.datetime.now().timestamp()) - 150
        ):
            return {
                "status": 1,
                "description": "iast-scanner not connected.",
                "data": [],
            }

    except IastScanner.DoesNotExist:
        return {
            "status": 1,
            "description": "IastScanner matching query does not exist.",
            "data": [],
        }

    data = service_get_target(
        api_url=iast_scanner_url, page=body.page, perpage=body.perpage
    )

    if data:
        return data
    else:
        return {"status": 2, "description": "not found target", "data": []}


@router.post("/new")
def new_or_start_target(request, body: TargetFilterSchema):
    logger.debug(body)
    if not body.app_id:
        return {
            "status": 1,
            "description": "app_id does not exist.",
            "data": [],
        }
    # 根据 body.app_id 查询iast扫描器监听接口地址
    try:
        iast_scanner = IastScanner.objects.get(app_id=body.app_id)
        iast_scanner_url = iast_scanner.url

        # 如果状态为假或者超时，直接返回
        if (
            not iast_scanner.status
            or iast_scanner.heartbeat_time
            < int(datetime.datetime.now().timestamp()) - 150
        ):
            return {
                "status": 1,
                "description": "iast-scanner not connected.",
                "data": [],
            }

    except IastScanner.DoesNotExist:
        return {
            "status": 1,
            "description": "IastScanner matching query does not exist.",
            "data": [],
        }

    data = service_new_or_start_target(
        api_url=iast_scanner_url, host=body.host, port=body.port
    )

    if data:
        return data
    else:
        return {"status": 2, "description": "not found response", "data": []}


@router.post("/kill")
def kill(request, body: TargetFilterSchema):
    logger.debug(">>>>>>>>>>>>>>>>>>>>>", body=body)
    if body.app_id is None or body.scanner_id is None:
        return {
            "status": 1,
            "description": "app_id or scanner_id does not exist.",
            "data": [],
        }
    # 根据 body.app_id 查询iast扫描器监听接口地址
    try:
        iast_scanner = IastScanner.objects.get(app_id=body.app_id)
        iast_scanner_url = iast_scanner.url

        # 如果状态为假或者超时，直接返回
        if (
            not iast_scanner.status
            or iast_scanner.heartbeat_time
            < int(datetime.datetime.now().timestamp()) - 150
        ):
            return {
                "status": 1,
                "description": "iast-scanner not connected.",
                "data": [],
            }

    except IastScanner.DoesNotExist:
        return {
            "status": 1,
            "description": "IastScanner matching query does not exist.",
            "data": [],
        }

    data = service_stop_scanning_target(
        api_url=iast_scanner_url, scanner_id=body.scanner_id
    )

    if data:
        return data
    else:
        return {"status": 2, "description": "not found response", "data": []}


@router.post("/clean")
def clean_target(request, body: TargetFilterSchema):
    logger.debug(">>>>>>>>>>>>>>>>>>>>>", body=body)
    if not body.app_id:
        return {
            "status": 1,
            "description": "app_id does not exist.",
            "data": [],
        }
    # 根据 body.app_id 查询iast扫描器监听接口地址
    try:
        iast_scanner = IastScanner.objects.get(app_id=body.app_id)
        iast_scanner_url = iast_scanner.url

        # 如果状态为假或者超时，直接返回
        if (
            not iast_scanner.status
            or iast_scanner.heartbeat_time
            < int(datetime.datetime.now().timestamp()) - 150
        ):
            return {
                "status": 1,
                "description": "iast-scanner not connected.",
                "data": [],
            }

    except IastScanner.DoesNotExist:
        return {
            "status": 1,
            "description": "IastScanner matching query does not exist.",
            "data": [],
        }

    data = service_clean_target(
        api_url=iast_scanner_url, host=body.host, port=body.port, url_only=body.url_only
    )

    if data:
        return data
    else:
        return {"status": 2, "description": "not found response", "data": []}
