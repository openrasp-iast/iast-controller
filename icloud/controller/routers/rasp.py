from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from django.db.models import Q


from ninja import Router

from controller.schemas import RaspFilterSchema
from agent.models import Rasp

import structlog

logger = structlog.get_logger(__name__)

router = Router()


@router.post("/get")
def get_rasp(request, body: RaspFilterSchema):
    """
    Rasp查询接口
    """

    logger.info("get_rasp", body=body)

    query = (
        Q(hostname__icontains=body.keyword)
        | Q(description__icontains=body.keyword)
        | Q(register_ip__icontains=body.keyword)
        | Q(language__icontains=body.keyword)
    )
    if body.app_id and body.keyword:
        rasps = Rasp.objects.filter(app_id=body.app_id)
        rasps = rasps.filter(query)
    elif body.keyword:
        rasps = Rasp.objects.filter(query)
    else:
        rasps = Rasp.objects.all()

    page = body.page or 1
    perpage = body.perpage or 5

    # 创建一个Paginator对象，每页显示10个对象
    paginator = Paginator(rasps.order_by("register_time"), perpage)

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
    rasps = [model_to_dict(rasp) for rasp in current_page.object_list]

    return {
        "status": 0,
        "description": "ok",
        "data": rasps,
        "total": paginator.count,
        "page": page,
        "perpage": perpage,
    }
