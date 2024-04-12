import jwt
from datetime import datetime, timedelta

from icloud.settings import SECRET_KEY


def create_jwt_token(user_id):
    payload = {
        "user_id": user_id,  # 用户唯一标识
        "exp": datetime.utcnow() + timedelta(days=1),  # 设置过期时间
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        # 令牌过期
        return None
    except jwt.InvalidTokenError:
        # 无效令牌
        return None
