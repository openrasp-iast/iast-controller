import datetime
from django.http import HttpRequest
from ninja import Router

from icloud.auth import ApiKey, ApiToken

from iast.models import Flow
from iast.util import hash_string
from iast.routers.task import router as task_router

import structlog


logger = structlog.get_logger(__name__)


router = Router(auth=ApiToken())
router.add_router("task", task_router)


@router.post("/flow", auth=None)
def flow(request: HttpRequest):
    logger.info(request.headers)
    logger.info(request.body)

    try:
        flow = Flow()
        flow.data = request.body.decode()
        flow.data_hash = hash_string(flow.data)
        flow.time = int(datetime.datetime.now().timestamp())
        flow.save()
    except Exception as e:
        logger.error(e)
        return {
            "data": {},
            "description": "error",
            "status": 1,
        }

    return {
        "data": {},
        "description": "ok",
        "status": 0,
    }


@router.post("/auth", auth=ApiKey())
def auth(request: HttpRequest):
    """
    {
        'Proxy': 'http://127.0.0.1:10809',
        'Content-Length': '2',
        'Content-Type': 'application/json',
        'Host': '192.168.31.30:8080',
        'User-Agent': 'python-requests/2.21.0',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'X-Openrasp-Appsecret': '1UDTwKcN1ak0smftbSyrDPpLOGUz5coIxAUmf0r9ZsEa',
        'X-Openrasp-Appid': '47014b167a616f646a788a6d9eb4a1a29ca98dda'
    }
    """
    logger.info(request.headers)
    logger.info(request.body)

    return {"status": 0, "description": "ok"}
