from ninja import Router

from icloud.auth import ApiToken

from controller.routers.user import router as user_router
from controller.routers.plugin import router as plugin_router
from controller.routers.app import router as app_router
from controller.routers.vuln import router as vuln_router
from controller.routers.dependency import router as dependency_router
from controller.routers.rasp import router as rasp_router
from controller.routers.dashboard import router as dashboard_router
from controller.routers.config import router as setting_router


router = Router(auth=ApiToken())
router.add_router("user", user_router)
router.add_router("plugin", plugin_router)
router.add_router("app", app_router)
router.add_router("vuln", vuln_router)
router.add_router("dependency", dependency_router)
router.add_router("rasp", rasp_router)
router.add_router("dashboard", dashboard_router)
router.add_router("setting", setting_router)


@router.api_operation(["GET", "POST"], "/ping", auth=None)
def ping(request):
    return {"data": {}, "description": "ok", "status": 0}


@router.post("/version", auth=None)
def version(request):
    return {
        "data": {
            "version": "1.3.5",
            "build_time": "2020-09-02 17:35:04",
            "commit_id": "055ddf48c789cd776c06c52307c716156b9f6048",
        },
        "description": "ok",
        "status": 0,
    }
