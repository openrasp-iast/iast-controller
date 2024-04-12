from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'v1/iast/order', consumers.OrderConsumer.as_asgi()),
]
