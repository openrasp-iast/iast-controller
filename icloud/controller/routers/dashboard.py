from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models import Q


from ninja import Router

from controller.schemas import AppFilterSchema

import structlog

from agent.models import IastScannerEvent

logger = structlog.get_logger(__name__)

router = Router()


@router.post("/type")
def get_vuln_type(request, body: AppFilterSchema):
    """ """
    logger.debug("get_vuln_type", body=body.app_id)

    option = {
        "title": {
            "text": "漏洞类型分布",
            "subtext": "基于APP统计",
            "left": "center",
        },
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "left": "left"},
        "series": [
            {
                # "name": "未发现漏洞",
                "type": "pie",
                "radius": "50%",
                "data": [],
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
            }
        ],
    }

    if not body.app_id:
        return {
            "status": 1,
            "description": "app_id does not exist.",
            "data": option,
        }

    # 统计
    attack_type_and_counts = IastScannerEvent.objects.values(
        "attack_type_name"
    ).annotate(count=Count("attack_type_name"))

    attack_type_list = list()
    for item in attack_type_and_counts:
        attack_type_list.append(
            {"value": item["count"], "name": item["attack_type_name"]}
        )
    option["series"][0]["data"] = attack_type_list
    return {"status": 0, "description": "success", "data": option}


@router.post("/trend")
def get_vuln_trend(request, body: AppFilterSchema):
    """ """
    # 获取当前日期
    current_date = datetime.now()

    # 生成过去 31 天的日期列表
    date_list = [
        (current_date - timedelta(days=i)).strftime("%m-%d") for i in range(30, -1, -1)
    ]

    option = {
        "title": {
            "text": "漏洞趋势变化",
            "subtext": "基于APP统计31天数据",
            "left": "center",
        },
        "tooltip": {"trigger": "item"},
        # 一个月的时间范围
        "xAxis": {
            "type": "category",
            "data": date_list,
            "axisLabel": {
                "rotate": 45,  # 设置横坐标标签旋转45
            },
        },
        "yAxis": {"type": "value"},
        "series": [{"data": [i for i in range(1, 32)], "type": "line"}],
    }

    if not body.app_id:
        return {
            "status": 1,
            "description": "app_id does not exist.",
            "data": option,
        }

    # 当前日期
    current_date = datetime.now()

    # 生成最近31天的日期列表
    date_list = [
        (current_date - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(31)
    ]

    # 首先获取数据库中存在的日期及其计数
    existing_counts = (
        IastScannerEvent.objects.filter(
            event_date__in=[
                datetime.strptime(date, "%Y-%m-%d").date() for date in date_list
            ]
        )
        .values("event_date")
        .annotate(count=Count("id"))
        .order_by("-event_date")
    )

    # 转换查询结果为字典，便于查找
    existing_counts_dict = {
        item["event_date"]: item["count"] for item in existing_counts
    }

    # 准备最终的计数结果列表，包括未出现的日期计数为0
    final_counts = []
    for date in date_list:
        # print(date)
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        count = existing_counts_dict.get(
            date_obj, 0
        )  # 如果日期不存在于existing_counts_dict中，则计数为0
        final_counts.append({"event_date": date_obj, "count": count})

    # 对列表按日期从小到大排序
    events_sorted = sorted(final_counts, key=lambda x: x["event_date"])

    # 拆分为日期和计数两个列表
    event_dates = [event["event_date"] for event in events_sorted]
    event_counts = [event["count"] for event in events_sorted]

    option["xAxis"]["data"] = event_dates
    option["series"][0]["data"] = event_counts

    return {"status": 0, "description": "success", "data": option}
