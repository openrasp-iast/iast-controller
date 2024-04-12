import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

import json

import structlog


logger = structlog.get_logger(__name__)


class OrderConsumer(AsyncWebsocketConsumer):
    """
    TODO API KEY 校验
    """

    # 跟踪所有活动连接的集合
    active_connections = set()

    async def connect(self):
        self.active_connections.add(self)
        logger.debug(f"Connections: {len(self.active_connections)}")

        await self.accept()

    async def disconnect(self, close_code):
        self.active_connections.discard(self)

    @database_sync_to_async
    def save_or_update_iast_scanner(self, info):

        try:
            from iast.models import IastScanner

            iast_scanner, _ = IastScanner.objects.get_or_create(
                app_id=info["app_id"],
                url=info["monitor_url"],
            )
            iast_scanner.app_id = info["app_id"]
            iast_scanner.url = info["monitor_url"]
            iast_scanner.heartbeat_time = int(datetime.datetime.now().timestamp())
            iast_scanner.status = True
            iast_scanner.save()

        except IastScanner.MultipleObjectsReturned:
            logger.error("IastScanner MultipleObjectsReturned")

    async def receive(self, text_data):
        if "monitor_url" in text_data:
            info = json.loads(text_data)

            await self.save_or_update_iast_scanner(info)
