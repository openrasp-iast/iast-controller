from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from django.db.models import Q


from ninja import Router

from controller.schemas import DependencyFilterSchema
from agent.models import Dependency

import structlog

logger = structlog.get_logger(__name__)

router = Router()



@router.post("/get")
def get_dependency(request, body: DependencyFilterSchema):
    """
    依赖库信息查询接口
    """
    
    logger.info("get_dependency", body=body)
    
    query = Q(product__icontains=body.keyword)  \
        | Q(version__icontains=body.keyword) \
        | Q(vendor__icontains=body.keyword) \
        | Q(source__icontains=body.keyword) \
    
    if body.app_id and body.keyword:
        deps = Dependency.objects.filter(app_id=body.app_id)
        deps = deps.filter(query)
    elif body.keyword:
        deps = Dependency.objects.filter(query)
    else:
        deps = Dependency.objects.all()

    page = body.page or 1
    perpage = body.perpage or 5

    # 创建一个Paginator对象，每页显示10个对象
    paginator = Paginator(deps.order_by("create_time"), perpage)

    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
            return {
        "status": -1,
        "description": "Invalid page number",
        "data": {},
        "total": paginator.count,
        "page": 1,
        "perpage": perpage,
    }
    # 获取第一页的内容
    deps = [model_to_dict(dep) for dep in current_page.object_list]

    return {
        "status": 0,
        "description": "ok",
        "data": deps,
        "total": paginator.count,
        "page": page,
        "perpage": perpage,
    }