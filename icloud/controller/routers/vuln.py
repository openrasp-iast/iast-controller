from django.core.paginator import Paginator
from django.forms.models import model_to_dict


from ninja import Router

from controller.models import App
from controller.schemas import VulnFilterSchema, AppSchema
from agent.models import IastScannerEvent

router = Router()


@router.post("/get")
def get_vuln(request, body: VulnFilterSchema):
    # lookup by vuln_id & app_id
    if body.app_id and body.vuln_id:
        try:
            event = IastScannerEvent.objects.filter(
                vuln_id=body.vuln_id, app_id=body.app_id.strip()
            ).first()
            if not event:
                return {
                    "status": 2,
                    "description": "result not found.",
                }
            return {"status": 0, "description": "ok", "data": model_to_dict(event)}
        except IastScannerEvent.DoesNotExist:
            return {
                "status": 1,
                "description": "IastScannerEvent matching query does not exist.",
            }

    # lookup by app_name 模糊查询
    if body.keyword:
        events = IastScannerEvent.objects.filter(
            plugin_name__icontains=body.keyword, app_id=body.app_id.strip()
        ).order_by("-event_time")
    else:
        events = IastScannerEvent.objects.all().filter(app_id=body.app_id.strip()).order_by("-event_time")

    page = body.page or 1
    perpage = body.perpage or 5

    # 创建一个Paginator对象，每页显示10个对象
    paginator = Paginator(events, perpage)

    # 获取第一页的内容
    events = [model_to_dict(event) for event in paginator.page(page).object_list]

    return {
        "status": 0,
        "description": "ok",
        "data": events,
        "total": paginator.count,
        "page": page,
        "perpage": perpage,
    }


@router.post("/create")
def create_app(request, body: AppSchema):
    print(body)
    app = App(
        name=body.app_name, language=body.app_language, description=body.app_description
    )
    app.save()
    return {"status": 0, "description": "ok", "data": model_to_dict(app)}


@router.post("/update")
def update_app(request, body: AppSchema):
    try:
        app = App.objects.get(id=body.id)
        app.name = body.name
        app.description = body.description
        app.save()
        return {"status": 0, "description": "ok", "data": model_to_dict(app)}
    except App.DoesNotExist:
        return {"status": 1, "description": "app not found"}


@router.post("/delete")
def delete_app(request, body: AppSchema):
    try:
        app = App.objects.get(id=body.id)
        app.delete()
        return {"status": 0, "description": "ok"}
    except App.DoesNotExist:
        return {"status": 1, "description": "app not found"}


# @router.get("/list")
# def get_apps(request, page: int = 1, perpage: int = 10):
#     # 查询所有应用
#     apps = App.objects.all()

#     # 分页
#     paginator = Paginator(apps, perpage)

#     # 获取第一页的内容
#     apps = [model_to_dict(app) for app in paginator.page(page).object_list]

#     return {"status": 0, "description": "ok", "data": apps}


@router.get("/detail")
def get_app_detail(request, app_id: int):
    try:
        app = App.objects.get(id=app_id)
        return {"status": 0, "description": "ok", "data": model_to_dict(app)}
    except App.DoesNotExist:
        return {"status": 1, "description": "app not found"}
