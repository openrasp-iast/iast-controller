from ninja.security import APIKeyHeader
from controller.services.jwt import decode_jwt_token
from controller.models import App


class ApiToken(APIKeyHeader):
    param_name = "X-OpenRASP-Token"

    def authenticate(self, request, token):
        try:
            payload = decode_jwt_token(token)
            if payload:
                return payload  # 或者返回一个用户对象
            else:
                return None
        except Exception:
            return None


class ApiKey(APIKeyHeader):
    param_name = "X-OpenRASP-AppSecret"

    def authenticate(self, request, secret):
        app_id = request.headers.get("X-OpenRASP-AppID")

        # 判断数据库表 App 中是否存在 app_id 和 secret 的记录
        if App.objects.filter(id=app_id, secret=secret).exists():
            return app_id
        return None

