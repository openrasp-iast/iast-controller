from django.core.paginator import Paginator
from django.forms.models import model_to_dict


from ninja import Router

from controller.models import App
from controller.schemas import AppFilterSchema, AppSchema

router = Router()



@router.post("/get")
def get_app(request, body: AppFilterSchema):
    # lookup by app_id
    if body.app_id:
        try:
            app = App.objects.get(id=body.app_id)
            return {"status": 0, "description": "ok", "data": model_to_dict(app)}
        except App.DoesNotExist:
            return {"status": 1, "description": "app not found"}

    # lookup by app_name 模糊查询
    if body.app_name:
        apps = App.objects.filter(name__icontains=body.app_name)
    else:
        apps = App.objects.all()

    page = body.page or 1
    perpage = body.perpage or 5

    # 创建一个Paginator对象，每页显示10个对象
    paginator = Paginator(apps, perpage)

    # 获取第一页的内容
    apps = [model_to_dict(app) for app in paginator.page(page).object_list]

    return {
        "status": 0,
        "description": "ok",
        "data": apps,
        "total": paginator.count,
        "page": page,
        "perpage": perpage,
    }


@router.post("/create")
def create_app(request, body: AppSchema):
    print(body)
    app = App(name=body.app_name, language=body.app_language,
              description=body.app_description)
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
