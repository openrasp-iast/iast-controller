import datetime
import json
from ninja import Router
from agent.schemas import Error, Policy
from agent.models import IastScannerEvent

import structlog

from agent.util.vuln_map import VulnStatusMap, VulnTypeMap


logger = structlog.get_logger(__name__)

router = Router()


@router.post("/error")
def error(request, body: Error):
    logger.info(body)
    # 成功处理的日志数量
    count = 0
    for error in body:
        logger.info(error)
        count += 1
    return {"status": 0, "description": "ok", "data": {"count": count}}


@router.post("/policy")
def policy(request, body: Policy):
    logger.info(body)
    # 成功处理的日志数量
    count = 0
    for error in body:
        logger.info(error)
        count += 1
    return {"status": 0, "description": "ok", "data": {"count": count}}


@router.post("/attack")
def attack(request):
    body = json.loads(request.body)
    logger.debug(type(body))

    for event in body:
        # logger.info(json.dumps(event))
        vuln, created = IastScannerEvent.objects.get_or_create(
            rasp_id=event["rasp_id"], request_id=event["request_id"], defaults=event
        )
        if not created:
            logger.debug("update vuln")
            vuln.count = vuln.count + 1
        # 获取日期
        event_time_obj = datetime.datetime.strptime(
            vuln.event_time, "%Y-%m-%dT%H:%M:%S%z"
        )
        vuln.event_date = event_time_obj.date()
        vuln.attack_type_name = VulnTypeMap[vuln.attack_type] or vuln.attack_type
        vuln.vuln_state = VulnStatusMap[vuln.intercept_state] or vuln.intercept_state
        vuln.save()

    return {"status": 0, "description": "ok"}
