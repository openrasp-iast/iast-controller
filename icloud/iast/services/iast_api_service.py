import requests


import structlog


logger = structlog.get_logger(__name__)


def _post_for_iast_scanner(api_url, data):
    try:
        resp = requests.post(
            api_url, json=data, headers={"Content-Type": "application/json"}
        )
        if resp.status_code != 200:
            logger.error("Failed to get target", status_code=resp.status_code)
            raise Exception("Failed to get target")
    except Exception as e:
        logger.error("Failed to get target", error=e)
        return {
            "status": 1,
            "description": "Failed to get target.",
            "data": [],
        }
    return resp.json()


def service_get_target(api_url, page=1, perpage=10):
    """
    获取所有目标的扫描任务
    """
    return _post_for_iast_scanner(api_url + "/api/model/get_all", {"page": page})


def service_new_or_start_target(api_url, host: str, port: int):
    """
    创建或启动扫描任务
    return {
        "status": 0,
        "description": "ok"
    }
    """
    return _post_for_iast_scanner(
        api_url + "/api/scanner/new", {"host": host, "port": port}
    )


def service_stop_scanning_target(api_url, scanner_id: int):
    """
    停止指定ID的扫描任务
    return {
        "status": 0,
        "description": "ok"
    }
    """
    return _post_for_iast_scanner(
        api_url + "/api/scanner/kill", {"scanner_id": scanner_id}
    )


def service_clean_target(api_url, host: str, port: int, url_only: bool):
    """
    清除队列 / 删除任务
    return {
        "status": 0,
        "description": "ok"
    }
    """
    return _post_for_iast_scanner(
        api_url + "/api/model/clean_target",
        {"host": host, "port": port, "url_only": url_only},
    )
